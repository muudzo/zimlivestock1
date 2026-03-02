"""
Payments API router — /payments
Handles Paynow transaction initiation, webhook callbacks, and status polling.
"""
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models import LivestockItem, Payment, User
from app.services import (
    check_payment_status,
    initiate_mobile_payment,
    initiate_web_payment,
)

router = APIRouter(prefix="/payments", tags=["payments"])


# ─── Request / Response Schemas ───────────────────────────────────────────────

class InitiatePaymentRequest(BaseModel):
    livestock_id: int
    bid_id: int
    payer_id: int
    payment_method: str         # "web" | "ecocash" | "onemoney"
    phone: Optional[str] = None # Required for mobile payments


class PaymentStatusResponse(BaseModel):
    reference: str
    status: str
    paid: bool
    paynow_status: Optional[str] = None
    redirect_url: Optional[str] = None
    instructions: Optional[str] = None


class PaymentHistoryItem(BaseModel):
    id: int
    merchant_reference: str
    livestock_id: Optional[int]
    amount: float
    currency: str
    payment_method: Optional[str]
    status: str
    created_at: datetime
    paid_at: Optional[datetime]


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/initiate", response_model=PaymentStatusResponse)
def initiate_payment(
    body: InitiatePaymentRequest,
    session: Session = Depends(get_session),
):
    """
    Initiate a Paynow payment for a won auction.

    - For web payments (card / ZIPIT) → returns a redirect_url for the browser.
    - For mobile payments (ecocash / onemoney) → returns instructions for the phone USSD prompt.
    """
    # ── Validate livestock item ──
    item = session.get(LivestockItem, body.livestock_id)
    if not item:
        raise HTTPException(status_code=404, detail="Livestock item not found")

    # ── Validate payer ──
    payer = session.get(User, body.payer_id)
    if not payer:
        raise HTTPException(status_code=404, detail="User not found")

    # ── Build unique merchant reference ──
    unique_suffix = uuid.uuid4().hex[:8].upper()
    reference = f"ZL-{body.livestock_id}-{unique_suffix}"
    description = f"ZimLivestock: {item.title} (ID #{item.id})"
    amount = item.currentBid if item.currentBid > 0 else item.startingPrice

    # ── Create pending Payment record ──
    payment = Payment(
        payer_id=body.payer_id,
        livestock_id=body.livestock_id,
        bid_id=body.bid_id,
        amount=amount,
        currency="USD",
        merchant_reference=reference,
        payment_method=body.payment_method,
        status="pending",
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)

    try:
        if body.payment_method == "web":
            # Standard browser-based checkout
            result = initiate_web_payment(reference, payer.email, description, amount)
            payment.paynow_poll_url = result["poll_url"]
            payment.paynow_redirect_url = result.get("redirect_url")
            session.add(payment)
            session.commit()
            return PaymentStatusResponse(
                reference=reference,
                status="pending",
                paid=False,
                redirect_url=result.get("redirect_url"),
            )
        else:
            # Mobile (EcoCash / OneMoney)
            if not body.phone:
                raise HTTPException(
                    status_code=400,
                    detail="A phone number is required for mobile payments (ecocash/onemoney).",
                )
            result = initiate_mobile_payment(
                reference, payer.email, description, amount, body.phone, body.payment_method
            )
            payment.paynow_poll_url = result["poll_url"]
            payment.paynow_instructions = result.get("instructions")
            session.add(payment)
            session.commit()
            return PaymentStatusResponse(
                reference=reference,
                status="pending",
                paid=False,
                instructions=result.get("instructions"),
            )

    except EnvironmentError as e:
        # Missing Paynow credentials
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        # Paynow rejected the request
        payment.status = "failed"
        session.add(payment)
        session.commit()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def paynow_webhook(request: Request, session: Session = Depends(get_session)):
    """
    Paynow posts payment status updates to this URL.

    ⚠  This endpoint must be publicly accessible.
    Use ngrok (https://ngrok.com) for local development:
        ngrok http 8000
    Then set PAYNOW_RESULT_URL=https://<your-ngrok-id>.ngrok.io/payments/webhook
    """
    form_data = await request.form()
    data = dict(form_data)

    reference = data.get("reference", "")
    paynow_ref = data.get("paynowreference", "")
    status_raw = data.get("status", "").lower()

    # Find matching payment by our merchant reference
    stmt = select(Payment).where(Payment.merchant_reference == reference)
    payment = session.exec(stmt).first()

    if not payment:
        # Acknowledge so Paynow doesn't retry endlessly
        return {"received": True}

    # Map Paynow status strings → our internal statuses
    if status_raw in ("paid", "awaiting delivery", "delivered"):
        if payment.status != "paid":  # Idempotency guard
            payment.status = "paid"
            payment.paid_at = datetime.utcnow()
            payment.paynow_reference = paynow_ref

            # Optionally mark item as sold
            if payment.livestock_id:
                item = session.get(LivestockItem, payment.livestock_id)
                if item:
                    item.healthStatus = "sold"
                    session.add(item)

    elif status_raw in ("cancelled", "disputed"):
        payment.status = "cancelled"
    elif status_raw == "refunded":
        payment.status = "refunded"
    elif status_raw == "failed":
        payment.status = "failed"

    payment.updated_at = datetime.utcnow()
    session.add(payment)
    session.commit()

    return {"received": True}


@router.get("/status/{reference}", response_model=PaymentStatusResponse)
def get_payment_status(reference: str, session: Session = Depends(get_session)):
    """
    Check the current status of a payment by its merchant reference.
    Also polls Paynow live if we have a poll_url stored.
    """
    stmt = select(Payment).where(Payment.merchant_reference == reference)
    payment = session.exec(stmt).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    paynow_status_str = None

    if payment.paynow_poll_url and payment.status == "pending":
        try:
            result = check_payment_status(payment.paynow_poll_url)
            paynow_status_str = result["status"]

            # Sync our DB status if Paynow says it's paid
            if result["paid"] and payment.status != "paid":
                payment.status = "paid"
                payment.paid_at = datetime.utcnow()
                payment.updated_at = datetime.utcnow()
                session.add(payment)
                session.commit()
        except Exception:
            pass  # Don't fail the endpoint if the poll request itself fails

    return PaymentStatusResponse(
        reference=reference,
        status=payment.status,
        paid=payment.status == "paid",
        paynow_status=paynow_status_str,
        redirect_url=payment.paynow_redirect_url,
        instructions=payment.paynow_instructions,
    )


@router.get("/history/{user_id}")
def get_payment_history(user_id: int, session: Session = Depends(get_session)):
    """
    Returns all payments made by a given user (newest first).
    """
    payer = session.get(User, user_id)
    if not payer:
        raise HTTPException(status_code=404, detail="User not found")

    stmt = select(Payment).where(Payment.payer_id == user_id).order_by(Payment.created_at.desc())
    payments = session.exec(stmt).all()

    return [
        PaymentHistoryItem(
            id=p.id,
            merchant_reference=p.merchant_reference,
            livestock_id=p.livestock_id,
            amount=p.amount,
            currency=p.currency,
            payment_method=p.payment_method,
            status=p.status,
            created_at=p.created_at,
            paid_at=p.paid_at,
        )
        for p in payments
    ]
