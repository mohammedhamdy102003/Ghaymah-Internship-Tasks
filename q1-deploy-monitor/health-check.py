#!/usr/bin/env python3
"""
Monitoring script for Q1 - Ghaymah SRE exam.
Checks the deployed app's /health endpoint every 30 seconds,
logs status + response time to a CSV file, and prints live status
to the console.

Usage:
    python3 health-check.py https://your-app-url.ghaymah.systems
"""
import sys
import time
import csv
import os
from datetime import datetime, timezone
import urllib.request
import urllib.error

CHECK_INTERVAL_SECONDS = 30
LOG_FILE = "monitor-log.csv"


def check_health(url: str) -> dict:
    endpoint = url.rstrip("/") + "/health"
    start = time.time()
    try:
        with urllib.request.urlopen(endpoint, timeout=10) as response:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            status_code = response.getcode()
            return {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "UP" if status_code == 200 else "DEGRADED",
                "status_code": status_code,
                "response_time_ms": elapsed_ms,
            }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        elapsed_ms = round((time.time() - start) * 1000, 2)
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "DOWN",
            "status_code": None,
            "response_time_ms": elapsed_ms,
            "error": str(e),
        }


def log_result(result: dict):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        fieldnames = ["timestamp", "status", "status_code", "response_time_ms", "error"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({**{"error": ""}, **result})


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 health-check.py <app_url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Monitoring {url}/health every {CHECK_INTERVAL_SECONDS}s. Logging to {LOG_FILE}. Ctrl+C to stop.")

    try:
        while True:
            result = check_health(url)
            log_result(result)
            print(f"[{result['timestamp']}] {result['status']} "
                  f"({result['response_time_ms']}ms)"
                  + (f" - {result.get('error')}" if result.get("error") else ""))
            time.sleep(CHECK_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()

