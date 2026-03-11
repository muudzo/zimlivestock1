"""
Shared auth helpers used across all route blueprints.
"""
from functools import wraps
from flask import request, jsonify
from db import supabase


def require_auth(f):
    """Decorator that extracts and validates the Bearer token.
    Injects `current_user` as the first kwarg to the wrapped function."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not supabase:
            return jsonify({"detail": "Supabase not configured"}), 500

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"detail": "Missing or malformed token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            user_res = supabase.auth.get_user(token)
            kwargs["current_user"] = user_res.user
        except Exception:
            return jsonify({"detail": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    return decorated


def require_supabase(f):
    """Decorator that returns 500 early if Supabase is not configured."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not supabase:
            return jsonify({"detail": "Supabase not configured"}), 500
        return f(*args, **kwargs)
    return decorated
