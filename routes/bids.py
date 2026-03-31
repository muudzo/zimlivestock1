from flask import Blueprint, request, jsonify
from db import supabase
from middleware import require_auth, require_supabase

bids_bp = Blueprint("bids", __name__, url_prefix="/bids")


@bids_bp.route("/livestock/<int:livestock_id>", methods=["GET"])
@require_supabase
def get_bids(livestock_id):
    limit = request.args.get("limit", default=50, type=int)
    offset = request.args.get("offset", default=0, type=int)

    res = (
        supabase.table("bids")
        .select("*")
        .eq("livestock_id", livestock_id)
        .order("amount", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return jsonify(res.data)


@bids_bp.route("", methods=["POST"])
@require_auth
@rate_limit(limit=5, window=60) # Commit 8: Limit bids to 5 per minute
def place_bid(current_user=None):
    data = request.json
    if not data:
        return jsonify({"detail": "Request body required"}), 400

    livestock_id = data.get("livestock_id")
    amount = data.get("amount")

    if not livestock_id or not amount:
        return jsonify({"detail": "livestock_id and amount are required"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"detail": "Amount must be a positive number"}), 400

    try:
        # Commit 4: Use Atomic RPC to prevent race conditions
        res = supabase.rpc("place_bid_atomic", {
            "p_livestock_id": livestock_id,
            "p_amount": amount,
            "p_bidder_id": current_user.id
        }).execute()

        # If RPC fails or returns error, handle it (Supabase SDK might throw or return error in res)
        if not res.data:
            return jsonify({"detail": "Failed to place bid or bid too low"}), 400

        return jsonify(res.data), 201
    except Exception as e:
        error_msg = str(e)
        if "Bid must be higher" in error_msg:
             return jsonify({"detail": error_msg}), 400
        return jsonify({"detail": "Failed to place bid"}), 500
