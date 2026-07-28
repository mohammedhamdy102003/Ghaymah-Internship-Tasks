# Q2 – Incident Postmortem

## Scenario

The production API experienced repeated **OOMKilled** events, resulting in approximately **45 minutes** of service downtime.

This document provides a complete incident analysis, including the timeline, root cause, resolution steps, preventive actions, an auto-scaling strategy for Ghaymah Cloud, and an early detection approach using monitoring tools.

---

## Contents

- Incident Summary
- Impact Analysis
- Timeline
- Detection
- Root Cause Analysis
- Resolution
- Lessons Learned
- Preventive Actions
- Ghaymah Auto-Scaling Policy
- Early Detection Strategy

---

## Auto-Scaling on Ghaymah

The proposed scaling policy is designed for applications deployed on the **Ghaymah Container Platform**.

The application maintains at least two running replicas and automatically scales based on CPU and memory utilization.

Scaling thresholds:

- Scale Out:
  - CPU > 70%
  - Memory > 75%
  - Duration: 2 minutes

- Scale In:
  - CPU < 30%
  - Memory < 40%
  - Duration: 10 minutes

This configuration minimizes the probability of future OOMKilled incidents by distributing traffic across multiple container replicas.

---

## Monitoring Strategy

The application should be monitored using **Ghaymah Monitoring** together with the custom monitoring dashboard developed in Question 1.

The monitoring system continuously checks:

- Memory Usage
- CPU Usage
- Container Restart Count
- OOMKilled Events
- HTTP Response Time
- HTTP 5xx Error Rate
- `/health` Endpoint Status

Alerts are generated whenever abnormal resource utilization or unhealthy application status is detected.

---

## Conclusion

The incident was caused by excessive memory consumption that exceeded the container memory limit, resulting in repeated OOMKilled events.

The issue was resolved by rolling back to the previous stable deployment and verifying service recovery using the application's `/health` endpoint.

Future incidents can be mitigated through proactive monitoring, automated alerting, memory-based auto-scaling, and proper pre-production testing.
