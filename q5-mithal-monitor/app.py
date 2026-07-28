from flask import Flask, jsonify, render_template
import json
import os
import threading
import time
import monitor  # our monitor.py — reused directly, not run as a separate process

app = Flask(__name__)

DATA_FILE = "monitor-data.json"


def background_monitor_loop():
    """Runs monitor.monitor() every CHECK_INTERVAL seconds inside this
    same process/container, since the Dockerfile only starts one
    process (gunicorn running app.py). This replaces running
    monitor.py as a separate process, which never actually happened
    after deployment (only app.py ran, monitor.py was never invoked)."""
    print("Starting background monitor thread...")
    while True:
        try:
            monitor.monitor()
        except Exception as e:
            print("Monitor thread error:", e)
        time.sleep(monitor.CHECK_INTERVAL)


# Start the background thread once, when this module is imported by
# gunicorn. Safe because the Dockerfile runs a single gunicorn worker
# (no --workers flag => defaults to 1), so this thread won't be
# duplicated across multiple worker processes.
monitor_thread = threading.Thread(target=background_monitor_loop, daemon=True)
monitor_thread.start()


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/metrics")
def metrics():

    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return jsonify(data)


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
