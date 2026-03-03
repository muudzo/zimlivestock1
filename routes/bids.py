from flask import Blueprint, request, jsonify
import os
from supabase import create_client, Client

bids_bp = Blueprint('bids', __name__, url_prefix='/bids')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@bids_bp.route('/livestock/<int:livestock_id>', methods=['GET'])
def get_bids(livestock_id):
    if not supabase:
        return jsonify({"error": "Supabase not configured"}), 500
    
    res = supabase.table('bids').select('*').eq('livestock_id', livestock_id).order('amount', desc=True).execute()
    return jsonify(res.data)

@bids_bp.route('', methods=['POST'])
def place_bid():
    if not supabase:
        return jsonify({"error": "Supabase not configured"}), 500

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
    # Assign bidder_id from authenticated user
    data['bidder_id'] = user.id
    
    # Basic validation: check if higher than current highest bid
    try:
        current_bids = supabase.table('bids').select('amount').eq('livestock_id', data['livestock_id']).order('amount', desc=True).limit(1).execute()
        if current_bids.data and data['amount'] <= current_bids.data[0]['amount']:
            return jsonify({"detail": "Bid must be higher than the current highest bid"}), 400
            
        res = supabase.table('bids').insert(data).execute()
        return jsonify(res.data[0]), 201
    except Exception as e:
        return jsonify({"detail": str(e)}), 400
