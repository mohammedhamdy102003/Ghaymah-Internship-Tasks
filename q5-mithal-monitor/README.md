# Mithal Monitor

A Flask-based monitoring application that periodically collects website metrics and exposes them through REST APIs. The application is containerized with Docker and deployed on Ghaymah.

## Features

- Monitor website availability
- Measure DNS lookup time
- Measure HTTP latency
- Measure search latency
- Check SSL certificate expiration
- Store collected metrics
- REST API for health checks and metrics
- Dockerized deployment
- Deployed on Ghaymah

---

## Tech Stack

- Python
- Flask
- SQLite
- Docker
- Gunicorn
- Ghaymah

---

## API Endpoints

### Health Check

```http
GET /health
```

Example Response

```json
{
  "status": "healthy"
}
```

---

### Metrics

```http
GET /api/metrics
```

Example Response

```json
[
  {
    "timestamp": "2026-07-28 12:11:50",
    "uptime": true,
    "status_code": 200,
    "latency_ms": 34.03,
    "dns_ms": 2.38,
    "search_latency_ms": 108.42,
    "ssl_days_left": 49,
    "ssl_expiry": "2026-09-15"
  }
]
```

---

## Running Locally

Clone the repository

```bash
git clone <repo-url>
cd Q5-Mithal-Monitor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

The application will be available on

```
http://localhost:5000
```

---

## Docker

Build the image

```bash
docker build -t mithal-monitor .
```

Run the container

```bash
docker run -p 80:80 mithal-monitor
```

---

## Deployment

The application is deployed on Ghaymah.

Deployment URL:

```
https://mithal-monitor-74639f9fbe38.hosted.ghaymah.systems
```

Health Endpoint

```
https://mithal-monitor-74639f9fbe38.hosted.ghaymah.systems/health
```

Metrics Endpoint

```
https://mithal-monitor-74639f9fbe38.hosted.ghaymah.systems/api/metrics
```

---

## Project Structure

```
Q5-Mithal-Monitor/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── monitor.db
├── templates/
├── static/
├── .ghaymah.json
└── README.md
```

---

## Author

Mohammed Hamdy
