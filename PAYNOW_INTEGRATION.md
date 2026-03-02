# Paynow Integration Plan 💳

> **Goal**: Integrate [Paynow Zimbabwe](https://www.paynow.co.zw/) as the primary payment gateway for the ZimLivestock marketplace, enabling secure auction settlement, listing fees, and buyer payments.

---

## Table of Contents

1. [About Paynow](#about-paynow)
2. [Payment Flows](#payment-flows)
3. [Architecture Overview](#architecture-overview)
4. [Implementation Phases](#implementation-phases)
5. [New Database Models](#new-database-models)
6. [New API Endpoints](#new-api-endpoints)
7. [Code Examples](#code-examples)
8. [Security Considerations](#security-considerations)
9. [Testing Strategy](#testing-strategy)
10. [Dependencies to Add](#dependencies-to-add)

---

## About Paynow

[Paynow](https://www.paynow.co.zw/) is Zimbabwe's leading digital payment platform. It supports:

| Method | Description |
|---|---|
| **EcoCash** | Mobile money (most popular in Zimbabwe) |
| **OneMoney** | NetOne mobile money |
| **ZIPIT** | Bank transfer |
| **Visa/Mastercard** | Card payments |
| **Telecash** | Telecel mobile money |

Paynow provides a simple **merchant API** using HTTP POST requests (no official Python SDK, but easy to implement directly).

**Key credentials you will need** (obtain from [Paynow Merchant Portal](https://www.paynow.co.zw/merchant/management)):
- `PAYNOW_INTEGRATION_ID` — your merchant integration ID
- `PAYNOW_INTEGRATION_KEY` — your secret key for hash generation

---

## Payment Flows

### Flow 1: Auction Settlement (Primary)
> Triggered when an auction ends and the winning bidder must pay.

```
Auction Ends → Backend identifies winning bid → Sends payment request to winner
→ Winner pays via EcoCash/card → Paynow calls our webhook → Backend confirms payment
→ Seller is notified → Transaction recorded
```

### Flow 2: Listing Fee (Optional)
> Sellers pay a small fee to publish a premium listing.

```
Seller creates listing → Chooses premium tier → Redirected to Paynow checkout
→ Payment confirmed → Listing goes live with "Featured" badge
```

### Flow 3: Buy-It-Now (Future)
> Direct purchase without bidding, settled immediately via Paynow.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  ZimLivestock API                │
│                                                  │
│  ┌──────────────┐    ┌──────────────────────┐   │
│  │  /payments   │    │  Auction Scheduler   │   │
│  │  (Router)    │    │  (Background Task)   │   │
│  └──────┬───────┘    └──────────┬───────────┘   │
│         │                       │                │
│         └──────────┬────────────┘                │
│                    ▼                             │
│         ┌──────────────────┐                    │
│         │  PaynowService   │                    │
│         │  (HTTP Client)   │                    │
│         └──────────┬───────┘                    │
└──────────────────────────────────────────────────┘
                     │  HTTPS
                     ▼
          ┌─────────────────────┐
          │   Paynow API        │
          │  (paynow.co.zw)     │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │  Webhook Callback   │
          │  /payments/webhook  │◄── Paynow POSTs result here
          └─────────────────────┘
```

---

## Implementation Phases

### Phase 1 — Foundation (Week 1)
- [ ] Register ZimLivestock on the Paynow merchant portal
- [ ] Obtain `PAYNOW_INTEGRATION_ID` and `PAYNOW_INTEGRATION_KEY`
- [ ] Add `paynow-python` or implement raw HTTP client in `app/services/paynow.py`
- [ ] Add `Payment` and `Transaction` models to `models.py`
- [ ] Create `/payments` router and wire it up in `main.py`
- [ ] Implement `/payments/initiate` endpoint (creates a Paynow transaction)
- [ ] Implement `/payments/webhook` endpoint (handles Paynow callbacks)
- [ ] Store `PAYNOW_INTEGRATION_ID` and `PAYNOW_INTEGRATION_KEY` in `.env`

### Phase 2 — EcoCash Mobile Flow (Week 2)
- [ ] Implement mobile payments flow (EcoCash/OneMoney) via Paynow Express Checkout
- [ ] Add phone number collection on checkout (pre-filled from user profile)
- [ ] Handle polling for payment status (Paynow provides a `pollurl`)
- [ ] Send SMS/push notification to user on payment success/failure

### Phase 3 — Auction Settlement Automation (Week 3)
- [ ] Add background job (APScheduler or Celery) to detect ended auctions
- [ ] Automatically trigger payment request to the winning bidder
- [ ] Mark `LivestockItem` as `sold` once payment confirmed
- [ ] Notify seller with payment confirmation

### Phase 4 — Listing Fees & Dashboard (Week 4)
- [ ] Add listing fee tiers (Free / Standard / Featured)
- [ ] Build seller payment history dashboard
- [ ] Add payout/disbursement tracking for sellers

---

## New Database Models

Add the following to `app/models.py`:

```python
from typing import Optional, Literal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

PaymentStatus = Literal["pending", "paid", "failed", "cancelled", "refunded"]
PaymentMethod = Literal["ecocash", "onemoney", "telecash", "card", "zipit"]

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Who is paying
    payer_id: int = Field(foreign_key="user.id")
    
    # What they are paying for
    livestock_id: Optional[int] = Field(default=None, foreign_key="livestockitem.id")
    bid_id: Optional[int] = Field(default=None, foreign_key="bid.id")
    
    # Payment details
    amount: float                          # Amount in USD
    currency: str = "USD"
    payment_method: Optional[PaymentMethod] = None
    
    # Paynow fields
    paynow_reference: Optional[str] = None  # Paynow's transaction reference
    paynow_poll_url: Optional[str] = None   # URL to poll for status
    merchant_reference: str                 # Our internal reference (unique)
    
    # Status tracking
    status: PaymentStatus = "pending"
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None
    
    # Relationships
    payer: Optional["User"] = Relationship()
```

---

## New API Endpoints

Add to a new file `app/api/payments.py`:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/payments/initiate` | Start a Paynow payment for a won auction |
| `POST` | `/payments/webhook` | Receive Paynow payment status callbacks |
| `GET` | `/payments/status/{reference}` | Poll payment status manually |
| `GET` | `/payments/history` | Get a user's payment history |

---

## Code Examples

### 1. Paynow Service (`app/services/paynow.py`)

```python
import hashlib
import httpx
from urllib.parse import urlencode, parse_qs
from datetime import datetime
import os

PAYNOW_INIT_URL = "https://www.paynow.co.zw/interface/initiatetransaction"
PAYNOW_MOBILE_URL = "https://www.paynow.co.zw/interface/remotetransaction"

INTEGRATION_ID = os.getenv("PAYNOW_INTEGRATION_ID")
INTEGRATION_KEY = os.getenv("PAYNOW_INTEGRATION_KEY")
RESULT_URL = os.getenv("PAYNOW_RESULT_URL")   # Your webhook URL
RETURN_URL = os.getenv("PAYNOW_RETURN_URL")   # Where to redirect user after payment


def _generate_hash(values: dict, integration_key: str) -> str:
    """Generate SHA512 hash for request integrity."""
    hash_string = "".join(str(v) for v in values.values()) + integration_key
    return hashlib.sha512(hash_string.encode("utf-8")).hexdigest().upper()


def _verify_hash(data: dict, integration_key: str) -> bool:
    """Verify the hash on a Paynow callback."""
    received_hash = data.get("hash", "")
    data_without_hash = {k: v for k, v in data.items() if k != "hash"}
    expected_hash = _generate_hash(data_without_hash, integration_key)
    return received_hash.upper() == expected_hash


async def initiate_web_payment(reference: str, amount: float, email: str, description: str) -> dict:
    """
    Initiate a standard web-based Paynow payment.
    Returns redirect URL for the user to complete payment.
    """
    values = {
        "id": INTEGRATION_ID,
        "reference": reference,
        "amount": f"{amount:.2f}",
        "additionalinfo": description,
        "returnurl": RETURN_URL,
        "resulturl": RESULT_URL,
        "status": "Message",
        "authemail": email,
    }
    values["hash"] = _generate_hash(values, INTEGRATION_KEY)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            PAYNOW_INIT_URL,
            data=values,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        result = parse_qs(response.text)
        flat = {k: v[0] for k, v in result.items()}

    if flat.get("status", "").lower() != "ok":
        raise ValueError(f"Paynow initiation failed: {flat.get('error', 'Unknown error')}")

    return {
        "redirect_url": flat.get("browserurl"),
        "poll_url": flat.get("pollurl"),
        "paynow_reference": reference,
    }


async def initiate_mobile_payment(reference: str, amount: float, phone: str,
                                   method: str, description: str) -> dict:
    """
    Initiate an EcoCash/OneMoney/Telecash mobile payment.
    No browser redirect needed — user gets a USSD prompt on their phone.
    """
    values = {
        "id": INTEGRATION_ID,
        "reference": reference,
        "amount": f"{amount:.2f}",
        "additionalinfo": description,
        "returnurl": RETURN_URL,
        "resulturl": RESULT_URL,
        "status": "Message",
        "phone": phone,
        "method": method,  # "ecocash", "onemoney", "telecash"
    }
    values["hash"] = _generate_hash(values, INTEGRATION_KEY)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            PAYNOW_MOBILE_URL,
            data=values,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        result = parse_qs(response.text)
        flat = {k: v[0] for k, v in result.items()}

    if flat.get("status", "").lower() not in ("ok", "sent"):
        raise ValueError(f"Mobile payment failed: {flat.get('error', 'Unknown error')}")

    return {
        "poll_url": flat.get("pollurl"),
        "instructions": flat.get("instructions", "Check your phone for payment prompt."),
    }


async def poll_payment_status(poll_url: str) -> str:
    """
    Poll Paynow for the current payment status.
    Returns: 'Created' | 'Sent' | 'Cancelled' | 'Disputed' | 'Refunded' | 'Paid' | 'Awaiting%20Delivery' | 'Delivered'
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(poll_url)
        result = parse_qs(response.text)
        flat = {k: v[0] for k, v in result.items()}

    if not _verify_hash(flat, INTEGRATION_KEY):
        raise ValueError("Poll response hash verification failed")

    return flat.get("status", "Unknown")
```

### 2. Payments Router (`app/api/payments.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from app.database import get_session
from app.models import Payment, LivestockItem, User
from app.services.paynow import (
    initiate_web_payment,
    initiate_mobile_payment,
    poll_payment_status,
    _verify_hash,
    INTEGRATION_KEY
)
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from urllib.parse import parse_qs

router = APIRouter(prefix="/payments", tags=["payments"])


class InitiatePaymentRequest(BaseModel):
    livestock_id: int
    bid_id: int
    payer_id: int
    payment_method: str  # "web", "ecocash", "onemoney", "telecash"
    phone: Optional[str] = None  # Required for mobile payments


@router.post("/initiate")
async def initiate_payment(
    body: InitiatePaymentRequest,
    session: Session = Depends(get_session)
):
    item = session.get(LivestockItem, body.livestock_id)
    if not item:
        raise HTTPException(404, "Livestock item not found")

    payer = session.get(User, body.payer_id)
    if not payer:
        raise HTTPException(404, "User not found")

    # Create a unique merchant reference
    reference = f"ZL-{body.livestock_id}-{uuid.uuid4().hex[:8].upper()}"
    description = f"ZimLivestock: Payment for {item.title}"
    amount = item.currentBid

    # Create payment record
    payment = Payment(
        payer_id=body.payer_id,
        livestock_id=body.livestock_id,
        bid_id=body.bid_id,
        amount=amount,
        merchant_reference=reference,
        payment_method=body.payment_method if body.payment_method != "web" else None,
        status="pending",
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)

    try:
        if body.payment_method == "web":
            result = await initiate_web_payment(reference, amount, payer.email, description)
        else:
            if not body.phone:
                raise HTTPException(400, "Phone number required for mobile payments")
            result = await initiate_mobile_payment(
                reference, amount, body.phone, body.payment_method, description
            )

        # Save poll URL
        payment.paynow_poll_url = result.get("poll_url")
        session.commit()
        return {"payment_id": payment.id, "reference": reference, **result}

    except ValueError as e:
        payment.status = "failed"
        session.commit()
        raise HTTPException(400, str(e))


@router.post("/webhook")
async def paynow_webhook(request: Request, session: Session = Depends(get_session)):
    """
    Paynow calls this URL when a payment status changes.
    Must be publicly accessible (use ngrok for local testing).
    """
    form_data = await request.form()
    data = dict(form_data)

    # Verify hash integrity
    if not _verify_hash(data, INTEGRATION_KEY):
        raise HTTPException(400, "Invalid hash — possible tampering")

    reference = data.get("reference", "")
    status = data.get("status", "").lower()

    # Find matching payment
    from sqlmodel import select
    stmt = select(Payment).where(Payment.merchant_reference == reference)
    payment = session.exec(stmt).first()

    if not payment:
        return {"received": True}  # Acknowledge but ignore

    if status in ("paid", "awaiting delivery", "delivered"):
        payment.status = "paid"
        payment.paid_at = datetime.utcnow()

        # Mark listing as sold
        item = session.get(LivestockItem, payment.livestock_id)
        if item:
            item.healthStatus = "sold"  # or add a `status` field to LivestockItem
            session.add(item)

    elif status in ("cancelled", "disputed"):
        payment.status = "cancelled"
    elif status == "refunded":
        payment.status = "refunded"

    payment.paynow_reference = data.get("paynowreference")
    session.add(payment)
    session.commit()

    return {"received": True}


@router.get("/status/{reference}")
async def get_payment_status(reference: str, session: Session = Depends(get_session)):
    """Manually poll Paynow for the latest status of a payment."""
    from sqlmodel import select
    stmt = select(Payment).where(Payment.merchant_reference == reference)
    payment = session.exec(stmt).first()

    if not payment:
        raise HTTPException(404, "Payment not found")

    if payment.paynow_poll_url:
        paynow_status = await poll_payment_status(payment.paynow_poll_url)
        return {"reference": reference, "status": payment.status, "paynow_status": paynow_status}

    return {"reference": reference, "status": payment.status}
```

### 3. Register the Router (`app/main.py` — add these lines)

```python
from app.api import payments  # Add this import

app.include_router(payments.router)  # Add this line
```

### 4. Environment Variables (`.env`)

```dotenv
PAYNOW_INTEGRATION_ID=your_integration_id_here
PAYNOW_INTEGRATION_KEY=your_integration_key_here
PAYNOW_RESULT_URL=https://yourdomain.co.zw/payments/webhook
PAYNOW_RETURN_URL=https://yourdomain.co.zw/payment-success
```

---

## Security Considerations

| Risk | Mitigation |
|---|---|
| Webhook spoofing | Always verify SHA512 hash on every Paynow callback |
| Key exposure | Store keys in `.env`, never commit to git |
| Double payment | Use `merchant_reference` uniqueness constraint in DB |
| Amount tampering | Always read price from DB, never trust client-submitted amount |
| Replay attacks | Check `payment.status != "paid"` before processing a callback |
| MITM | Enforce HTTPS in production, reject HTTP callbacks |

> ⚠️ **Important**: Add `.env` to `.gitignore` immediately. Never hardcode your Paynow Integration Key in source code.

---

## Testing Strategy

### Local Testing with Ngrok

Paynow needs a publicly accessible webhook URL. Use `ngrok` during development:

```bash
# Start your API
uvicorn app.main:app --reload --port 8000

# In another terminal, start ngrok
ngrok http 8000

# Use the ngrok HTTPS URL as your PAYNOW_RESULT_URL:
# e.g. https://abc123.ngrok.io/payments/webhook
```

### Paynow Test Environment

Paynow provides a **test/sandbox mode**. Use test integration credentials from the merchant portal. Test transactions will not move real money.

### Test Cases to Cover

| Scenario | Expected Outcome |
|---|---|
| Successful EcoCash payment | `payment.status = "paid"`, listing marked as sold |
| User cancels payment | `payment.status = "cancelled"` |
| Webhook with invalid hash | Returns 400, no DB changes |
| Duplicate webhook received | Idempotent — no double-processing |
| Poll before payment confirmed | Returns "Sent" or "Created" |
| Poll after payment confirmed | Returns "Paid" |

---

## Dependencies to Add

Update `requirements.txt`:

```
fastapi
uvicorn
sqlmodel
pydantic
python-multipart
python-jose[cryptography]
passlib[bcrypt]
httpx
python-dotenv      # NEW: load .env variables
apscheduler        # NEW: background jobs for auction settlement
```

Install:
```bash
pip install python-dotenv apscheduler
```

---

## References

- [Paynow Zimbabwe Developer Docs](https://developers.paynow.co.zw/docs/)
- [Paynow Merchant Portal](https://www.paynow.co.zw/merchant/management)
- [Paynow API Reference (Web Payments)](https://developers.paynow.co.zw/docs/core_doc.html)
- [Paynow Mobile Payments](https://developers.paynow.co.zw/docs/express_checkout.html)

---

*Integration plan v1.0 — ZimLivestock Team 🇿🇼*
