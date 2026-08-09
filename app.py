import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify

# Load variables from .env for local development
load_dotenv()

app = Flask(__name__)


# Home endpoint
@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask!",
        "status": "running"
    }), 200


# Liveness probe
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Readiness probe
@app.route("/ready")
def ready():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        connection.close()

        return jsonify({
            "status": "ready",
            "database": "connected"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "not ready",
            "database": "disconnected",
            "error": str(e)
        }), 503


# Start Flask application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )