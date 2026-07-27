"""
Simple API app for Ghaymah SRE exam - Q1
Provides:
  GET /            -> basic info
  GET /health      -> health check endpoint (used by monitoring)
  GET /metrics     -> simple JSON metrics (request count, uptime)
"""
import time
from flask import Flask, jsonify

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    # Allows the dashboard (served from a different origin, e.g. file://
    # or another host) to call this API from the browser.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

START_TIME = time.time()
REQUEST_COUNT = 0


@app.before_request
def count_requests():
    global REQUEST_COUNT
    REQUEST_COUNT += 1


@app.route("/")
def index():
    return jsonify({
        "service": "ghaymah-exam-api",
        "message": "API is running"
    })


@app.route("/health")
def health():
    """Used by ghaymah.systems platform + our monitoring script."""
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }), 200


@app.route("/metrics")
def metrics():
    return jsonify({
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "total_requests": REQUEST_COUNT
    })


if __name__ == "__main__":
    # 0.0.0.0 required so the container's port is reachable externally
    app.run(host="0.0.0.0", port=5000)
