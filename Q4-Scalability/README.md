# Q4 - Scalability & Load Balancing

## Objective

Design a scalable architecture capable of handling **15,000 requests per second** on the Ghaymah Container Platform.

---

## Proposed Architecture

The solution uses:

- Ghaymah Load Balancer
- 39 Application Containers
- PostgreSQL Database
- Redis Cache
- Ghaymah Block Storage
- Monitoring and Health Checks

The Load Balancer distributes incoming traffic evenly across all application containers while health checks ensure traffic is only routed to healthy instances.

---

## Container Calculation

Expected Traffic

- 15,000 requests/second

Container Capacity

- 500 requests/second

Required Containers

15000 / 500 = 30

Including 30% reserve capacity

30 × 1.3 = 39 containers

---

## Cold Start Strategy

The platform keeps additional warm containers available to reduce startup latency during sudden traffic spikes.

New containers are automatically created when resource utilization reaches the defined thresholds and are added to the Load Balancer only after passing health checks.

---

## Ghaymah Block Storage

Persistent storage is attached to the database layer to ensure application data survives container restarts and deployments.

Suitable workloads include:

- Databases
- Logs
- Uploaded files
- Stateful applications

---

## Monitoring

The deployment should continuously monitor:

- CPU Utilization
- Memory Usage
- Response Time
- Error Rate
- Container Health
- Restart Count

Alerts should be triggered before resources reach critical levels to prevent service interruption.
