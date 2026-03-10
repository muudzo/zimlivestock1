from flask import Blueprint, request, jsonify
import os
import uuid
from datetime import datetime
from supabase import create_client, Client
from services import (
    check_payment_status,
    initiate_mobile_payment,
    initiate_web_payment,
    verify_paynow_webhook
)

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@payments_bp.route('/initiate', methods=['POST'])
def initiate_payment():
    if not supabase:
        return jsonify({"detail": "Supabase not configured"}), 500

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"detail": "Not authenticated"}), 401
    
    token = auth_header.replace('Bearer ', '')
    try:
        user_res = supabase.auth.get_user(token)
        user = user_res.user
    except:
        return jsonify({"detail": "Invalid token"}), 401

    data = request.json
    livestock_id = data.get('livestock_id')
    bid_id = data.get('bid_id')
    payment_method = data.get('payment_method')
    phone = data.get('phone')

    # Validate item
    item_res = supabase.table('livestock_items').select('*').eq('id', livestock_id).single().execute()
    if not item_res.data:
        return jsonify({"detail": "Livestock item not found"}), 404
    
    item = item_res.data
    
    unique_suffix = uuid.uuid4().hex[:8].upper()
    reference = f"ZL-{livestock_id}-{unique_suffix}"
    description = f"ZimLivestock: {item['title']} (ID #{item['id']})"
    
    # Use currentBid or startingPrice
    amount = float(item.get('currentBid') or item.get('startingPrice') or 0)

    # Prepare pending payment record
    payment_data = {
        "payer_id": user.id,
        "livestock_id": livestock_id,
        "bid_id": bid_id,
        "amount": amount,
        "currency": "USD",
        "merchant_reference": reference,
        "payment_method": payment_method,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        if payment_method == "web":
            result = initiate_web_payment(reference, user.email, description, amount)
            payment_data["paynow_poll_url"] = result["poll_url"]
            payment_data["paynow_redirect_url"] = result.get("redirect_url")
            
            supabase.table('payments').insert(payment_data).execute()
            
            return jsonify({
                "reference": reference,
                "status": "pending",
                "paid": False,
                "redirect_url": result.get("redirect_url")
            }), 200
        else:
            if not phone:
                return jsonify({"detail": "Phone required for mobile"}), 400
                
            result = initiate_mobile_payment(reference, user.email, description, amount, phone, payment_method)
            payment_data["paynow_poll_url"] = result["poll_url"]
            payment_data["paynow_instructions"] = result.get("instructions")
            
            supabase.table('payments').insert(payment_data).execute()
            
            return jsonify({
                "reference": reference,
                "status": "pending",
                "paid": False,
                "instructions": result.get("instructions")
            }), 200
            
    except Exception as e:
        return jsonify({"detail": str(e)}), 400

@payments_bp.route('/webhook', methods=['POST'])
def paynow_webhook():
    # Flask form data
    data = request.form.to_dict()
    
    if not verify_paynow_webhook(data):
        return jsonify({"detail": "Invalid payment hash"}), 400
        
    reference = data.get("reference", "")
    paynow_ref = data.get("paynowreference", "")
    status_raw = data.get("status", "").lower()

    # Find matching payment
    pay_res = supabase.table('payments').select('*').eq('merchant_reference', reference).execute()
    if not pay_res.data:
        return jsonify({"received": True}), 200
    
    payment = pay_res.data[0]
    update_data = {"updated_at": datetime.utcnow().isoformat()}

    if status_raw in ("paid", "awaiting delivery", "delivered"):
        if payment['status'] != "paid":
            update_data["status"] = "paid"
            update_data["paid_at"] = datetime.utcnow().isoformat()
            update_data["paynow_reference"] = paynow_ref
            
            # Mark item as sold
            if payment['livestock_id']:
                supabase.table('livestock_items').update({"healthStatus": "sold"}).eq('id', payment['livestock_id']).execute()
    
    elif status_raw in ("cancelled", "disputed"):
        update_data["status"] = "cancelled"
    elif status_raw == "failed":
        update_data["status"] = "failed"

    supabase.table('payments').update(update_data).eq('merchant_reference', reference).execute()
    
    return jsonify({"received": True}), 200

@payments_bp.route('/status/<reference>', methods=['GET'])
def get_status(reference):
    pay_res = supabase.table('payments').select('*').eq('merchant_reference', reference).execute()
    if not pay_res.data:
        return jsonify({"detail": "Payment not found"}), 404
        
    payment = pay_res.data[0]
    paynow_status_str = None
    
    if payment.get('paynow_poll_url') and payment['status'] == "pending":
        try:
            result = check_payment_status(payment['paynow_poll_url'])
            paynow_status_str = result["status"]
            
            if result["paid"] and payment['status'] != "paid":
                update_data = {
                    "status": "paid",
                    "paid_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                supabase.table('payments').update(update_data).eq('merchant_reference', reference).execute()
                payment['status'] = "paid"
        except:
            pass

    return jsonify({
        "reference": reference,
        "status": payment['status'],
        "paid": payment['status'] == "paid",
        "paynow_status": paynow_status_str,
        "redirect_url": payment.get('paynow_redirect_url'),
        "instructions": payment.get('paynow_instructions')
    })

@payments_bp.route('/history', methods=['GET'])
def get_history():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"detail": "Not authenticated"}), 401
    
    token = auth_header.replace('Bearer ', '')
    try:
        user_res = supabase.auth.get_user(token)
        user = user_res.user
    except:
        return jsonify({"detail": "Invalid token"}), 401

    res = supabase.table('payments').select('*').eq('payer_id', user.id).order('created_at', desc=True).execute()
    return jsonify(res.data)
