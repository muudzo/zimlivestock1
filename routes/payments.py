import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from db import supabase
from middleware import require_auth, require_supabase
from services import (
    check_payment_status,
    initiate_mobile_payment,
    initiate_web_payment,
    verify_paynow_webhook,
)

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.route("/initiate", methods=["POST"])
@require_auth
@rate_limit(limit=3, window=60) # Commit 8: Limit payments to 3 per minute
def initiate_payment(current_user=None):
    data = request.json
    if not data:
        return jsonify({"detail": "Request body required"}), 400

    livestock_id = data.get("livestock_id")
    bid_id = data.get("bid_id")
    payment_method = data.get("payment_method")
    phone = data.get("phone")

    if not livestock_id or not payment_method:
        return jsonify({"detail": "livestock_id and payment_method are required"}), 400

    item_res = (
        supabase.table("livestock_items")
        .select("*")
        .eq("id", livestock_id)
        .single()
        .execute()
    )
    if not item_res.data:
        return jsonify({"detail": "Livestock item not found"}), 404

    idempotency_key = data.get("idempotency_key")
    
    # Commit 5: Check for existing payment with this idempotency key or bid_id
    if idempotency_key:
        existing = (
            supabase.table("payments")
            .select("*")
            .eq("idempotency_key", idempotency_key)
            .eq("payer_id", current_user.id)
            .execute()
        )
        if existing.data:
            payment = existing.data[0]
            return jsonify({
                "reference": payment["merchant_reference"],
                "status": payment["status"],
                "paid": payment["status"] == "paid",
                "redirect_url": payment.get("paynow_redirect_url"),
                "instructions": payment.get("paynow_instructions"),
            }), 200

    item = item_res.data
    # If no idempotency_key, we can still try to be idempotent based on bid_id if it's the same user
    if bid_id:
        existing_bid_pay = (
            supabase.table("payments")
            .select("*")
            .eq("bid_id", bid_id)
            .eq("status", "pending")
            .execute()
        )
        if existing_bid_pay.data:
            payment = existing_bid_pay.data[0]
            return jsonify({
                "reference": payment["merchant_reference"],
                "status": "pending",
                "paid": False,
                "redirect_url": payment.get("paynow_redirect_url"),
                "instructions": payment.get("paynow_instructions"),
            }), 200

    reference = f"ZL-{livestock_id}-{(idempotency_key or uuid.uuid4().hex)[:8].upper()}"
    description = f"ZimLivestock: {item['title']} (ID #{item['id']})"
    amount = float(item.get("currentBid") or item.get("startingPrice") or 0)

    if amount <= 0:
        return jsonify({"detail": "Invalid payment amount"}), 400

    payment_data = {
        "payer_id": current_user.id,
        "livestock_id": livestock_id,
        "bid_id": bid_id,
        "amount": amount,
        "currency": "USD",
        "merchant_reference": reference,
        "payment_method": payment_method,
        "status": "pending",
        "idempotency_key": idempotency_key,
        "created_at": datetime.utcnow().isoformat(),
    }

    try:
        if payment_method == "web":
            result = initiate_web_payment(reference, current_user.email, description, amount)
            payment_data["paynow_poll_url"] = result["poll_url"]
            payment_data["paynow_redirect_url"] = result.get("redirect_url")

            supabase.table("payments").insert(payment_data).execute()

            return jsonify({
                "reference": reference,
                "status": "pending",
                "paid": False,
                "redirect_url": result.get("redirect_url"),
            }), 200
        else:
            if not phone:
                return jsonify({"detail": "Phone required for mobile payment"}), 400

            result = initiate_mobile_payment(
                reference, current_user.email, description, amount, phone, payment_method
            )
            payment_data["paynow_poll_url"] = result["poll_url"]
            payment_data["paynow_instructions"] = result.get("instructions")

            supabase.table("payments").insert(payment_data).execute()

            return jsonify({
                "reference": reference,
                "status": "pending",
                "paid": False,
                "instructions": result.get("instructions"),
            }), 200

    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception:
        return jsonify({"detail": "Payment initiation failed"}), 500


@payments_bp.route("/webhook", methods=["POST"])
def paynow_webhook():
    data = request.form.to_dict()

    if not verify_paynow_webhook(data):
        return jsonify({"detail": "Invalid payment hash"}), 400

    reference = data.get("reference", "")
    paynow_ref = data.get("paynowreference", "")
    status_raw = data.get("status", "").lower()

    pay_res = (
        supabase.table("payments")
        .select("*")
        .eq("merchant_reference", reference)
        .execute()
    )
    if not pay_res.data:
        return jsonify({"received": True}), 200

    payment = pay_res.data[0]
    update_data = {"updated_at": datetime.utcnow().isoformat()}

    if status_raw in ("paid", "awaiting delivery", "delivered"):
        if payment["status"] != "paid":
            update_data["status"] = "paid"
            update_data["paid_at"] = datetime.utcnow().isoformat()
            update_data["paynow_reference"] = paynow_ref

            if payment["livestock_id"]:
                # Commit 9: Double check if already sold to ensure idempotency
                item_check = supabase.table("livestock_items").select("healthStatus").eq("id", payment["livestock_id"]).single().execute()
                if item_check.data and item_check.data.get("healthStatus") != "sold":
                    supabase.table("livestock_items").update(
                        {"healthStatus": "sold"}
                    ).eq("id", payment["livestock_id"]).execute()
    elif status_raw in ("cancelled", "disputed"):
        update_data["status"] = "cancelled"
    elif status_raw == "failed":
        update_data["status"] = "failed"

    # Only update if status actually changed or is pending (Commit 9)
    if payment["status"] == "pending" or "status" in update_data:
        supabase.table("payments").update(update_data).eq(
            "merchant_reference", reference
        ).execute()

    return jsonify({"received": True}), 200


@payments_bp.route("/status/<reference>", methods=["GET"])
@require_auth
def get_status(reference, current_user=None):
    pay_res = (
        supabase.table("payments")
        .select("*")
        .eq("merchant_reference", reference)
        .execute()
    )
    if not pay_res.data:
        return jsonify({"detail": "Payment not found"}), 404

    payment = pay_res.data[0]

    if payment["payer_id"] != current_user.id:
        return jsonify({"detail": "Not authorized to view this payment"}), 403

    paynow_status_str = None

    if payment.get("paynow_poll_url") and payment["status"] == "pending":
        try:
            result = check_payment_status(payment["paynow_poll_url"])
            paynow_status_str = result["status"]

            if result["paid"] and payment["status"] != "paid":
                update_data = {
                    "status": "paid",
                    "paid_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                }
                supabase.table("payments").update(update_data).eq(
                    "merchant_reference", reference
                ).execute()
                payment["status"] = "paid"
        except Exception:
            paynow_status_str = "check_failed"

    return jsonify({
        "reference": reference,
        "status": payment["status"],
        "paid": payment["status"] == "paid",
        "paynow_status": paynow_status_str,
        "redirect_url": payment.get("paynow_redirect_url"),
        "instructions": payment.get("paynow_instructions"),
    })


@payments_bp.route("/history", methods=["GET"])
@require_auth
def get_history(current_user=None):
    res = (
        supabase.table("payments")
        .select("*")
        .eq("payer_id", current_user.id)
        .order("created_at", desc=True)
        .execute()
    )
    return jsonify(res.data)
