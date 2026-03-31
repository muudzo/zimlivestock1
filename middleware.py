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


import time
from functools import wraps
from flask import request, jsonify

# Simple in-memory storage for rate limiting (Commit 8)
# In production, use Redis or Memcached for horizontal scalability.
rate_limit_storage = {}

def rate_limit(limit=10, window=60):
    """
    Simple rate limiting decorator.
    :param limit: Number of requests allowed
    :param window: Time window in seconds
    """
    def decorator(f):
         @wraps(f)
         def decorated_function(*args, **kwargs):
             ip = request.remote_addr
             now = time.time()
             
             # Clean up old entries for this IP
             if ip not in rate_limit_storage:
                 rate_limit_storage[ip] = []
             
             rate_limit_storage[ip] = [t for t in rate_limit_storage[ip] if now - t < window]
             
             if len(rate_limit_storage[ip]) >= limit:
                 return jsonify({"detail": "Too many requests. Please try again later."}), 429
             
             rate_limit_storage[ip].append(now)
             return f(*args, **kwargs)
         return decorated_function
    return decorator


def monitor_performance(f):
    """Decorator that logs the execution time of a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        duration = time.time() - start_time
        # Log to stdout (Scalability: in production, send to a monitoring service like Sentry or Datadog)
        print(f"[MONITOR] {request.method} {request.path} took {duration:.4f}s")
        return response
    return decorated_function


def require_supabase(f):
    """Decorator that returns 500 early if Supabase is not configured."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not supabase:
            return jsonify({"detail": "Supabase not configured"}), 500
        return f(*args, **kwargs)
    return decorated
