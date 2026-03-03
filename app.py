import os
from flask import Flask, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@app.route('/health')
def health():
    return jsonify({"status": "ok", "framework": "flask", "supabase_connected": supabase is not None})

# Import and register blueprints
from routes.auth import auth_bp
from routes.listings import listings_bp
from routes.bids import bids_bp

app.register_blueprint(auth_bp)
app.register_blueprint(listings_bp)
app.register_blueprint(bids_bp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, port=port)
