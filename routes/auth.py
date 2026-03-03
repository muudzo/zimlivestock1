from flask import Blueprint, request, jsonify
import os
from supabase import create_client, Client

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@auth_bp.route('/register', methods=['POST'])
def register():
    if not supabase:
        return jsonify({"detail": "Supabase not configured"}), 500
    
    data = request.json
    try:
        # Supabase Auth signup
        res = supabase.auth.sign_up({
            "email": data.get('email'),
            "password": data.get('password'),
            "options": {
                "data": {
                    "firstName": data.get('firstName'),
                    "lastName": data.get('lastName'),
                    "phone": data.get('phone')
                }
            }
        })
        
        # Also insert into public.profiles or similar if needed
        # For now, just return the user data from auth
        return jsonify(res.user), 201
    except Exception as e:
        return jsonify({"detail": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    if not supabase:
        return jsonify({"detail": "Supabase not configured"}), 500
    
    data = request.json
    try:
        res = supabase.auth.sign_in_with_password({
            "email": data.get('contact'), # Assuming contact is email for now
            "password": data.get('password')
        })
        return jsonify({
            "access_token": res.session.access_token,
            "token_type": "bearer",
            "user": res.user
        }), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 401

@auth_bp.route('/me', methods=['GET'])
def get_me():
    if not supabase:
        return jsonify({"detail": "Supabase not configured"}), 500
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"detail": "Missing token"}), 401
    
    token = auth_header.replace('Bearer ', '')
    try:
        # Get user from token
        res = supabase.auth.get_user(token)
        user = res.user
        # Normalize to the format frontend expects
        return jsonify({
            "id": user.id,
            "email": user.email,
            "firstName": user.user_metadata.get('firstName'),
            "lastName": user.user_metadata.get('lastName'),
            "phone": user.user_metadata.get('phone')
        }), 200
    except Exception as e:
        return jsonify({"detail": str(e)}), 401
