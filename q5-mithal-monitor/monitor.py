import requests
import socket
import ssl
import json
import os
import time
import dns.resolver

from datetime import datetime, UTC

# ===========================================
# Configuration
# ===========================================

BASE_URL = "https://mithal.space"
SEARCH_URL = "https://mithal.space/search?q=cloud"

OUTPUT_FILE = "monitor-data.json"

CHECK_INTERVAL = 60

# ===========================================
# HTTP Latency + Uptime
# ===========================================

def check_http():

    start = time.perf_counter()

    response = requests.get(BASE_URL, timeout=10)

    latency = (time.perf_counter() - start) * 1000

    return response.status_code, round(latency, 2)


# ===========================================
# Search Response
# ===========================================

def check_search():

    start = time.perf_counter()

    response = requests.get(SEARCH_URL, timeout=10)

    latency = (time.perf_counter() - start) * 1000

    return round(latency, 2)


# ===========================================
# DNS Lookup Time
# ===========================================

def check_dns():

    resolver = dns.resolver.Resolver()

    start = time.perf_counter()

    resolver.resolve("mithal.space")

    latency = (time.perf_counter() - start) * 1000

    return round(latency, 2)


# ===========================================
# SSL Certificate
# ===========================================

def check_ssl():

    hostname = "mithal.space"

    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=10) as sock:

        with context.wrap_socket(sock, server_hostname=hostname) as ssock:

            cert = ssock.getpeercert()

    expiry = datetime.strptime(
        cert["notAfter"],
        "%b %d %H:%M:%S %Y %Z"
    ).replace(tzinfo=UTC)

    days_left = (expiry - datetime.now(UTC)).days

    return expiry.strftime("%Y-%m-%d"), days_left


# ===========================================
# JSON
# ===========================================

def load_history():

    if not os.path.exists(OUTPUT_FILE):
        return []

    try:
        with open(OUTPUT_FILE, "r") as f:

            content = f.read().strip()

            if not content:
                return []

            return json.loads(content)

    except (json.JSONDecodeError, FileNotFoundError):

        return []


def save_history(data):

    with open(OUTPUT_FILE, "w") as f:

        json.dump(data, f, indent=4)


# ===========================================
# Monitoring
# ===========================================

def monitor():

    status_code, latency = check_http()

    ssl_expiry, ssl_days = check_ssl()

    entry = {

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "uptime": status_code == 200,

        "status_code": status_code,

        "latency_ms": latency,

        "dns_ms": check_dns(),

        "ssl_expiry": ssl_expiry,

        "ssl_days_left": ssl_days,

        "search_latency_ms": check_search()

    }

    history = load_history()

    history.append(entry)

    # آخر 24 ساعة (كل دقيقة)
    history = history[-1440:]

    save_history(history)

    print("=" * 60)
    print(json.dumps(entry, indent=4))


# ===========================================
# Main Loop
# ===========================================

if __name__ == "__main__":

    print("Starting Mithal Monitoring...")

    while True:

        try:

            monitor()

        except Exception as e:

            print("ERROR:", e)

        time.sleep(CHECK_INTERVAL)
