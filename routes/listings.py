from flask import Blueprint, request, jsonify
import os
from supabase import create_client, Client

listings_bp = Blueprint('listings', __name__, url_prefix='/livestock')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@listings_bp.route('', methods=['GET'])
def get_listings():
    if not supabase:
        return jsonify({"error": "Supabase not configured"}), 500
    
    category = request.args.get('category')
    query = supabase.table('livestock_items').select('*')
    
    if category:
        query = query.eq('category', category)
    
    res = query.execute()
    return jsonify(res.data)

@listings_bp.route('/<int:item_id>', methods=['GET'])
def get_listing(item_id):
    if not supabase:
        return jsonify({"error": "Supabase not configured"}), 500
        
    res = supabase.table('livestock_items').select('*, bids(*)').eq('id', item_id).single().execute()
    return jsonify(res.data)

@listings_bp.route('', methods=['POST'])
def create_listing():
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
    # Assign seller_id from authenticated user
    data['seller_id'] = user.id
    
    res = supabase.table('livestock_items').insert(data).execute()
    return jsonify(res.data[0]), 201
