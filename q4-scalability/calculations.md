# Container Capacity Calculation

## Given

- Expected Traffic = 15,000 requests/second
- One container capacity = 500 requests/second
- Required headroom = 30%

---

## Step 1

Number of containers without headroom

15000 / 500 = 30 Containers

---

## Step 2

Adding 30% reserve capacity

30 × 1.30 = 39 Containers

---

## Final Result

The application should run **39 containers** to safely handle the expected traffic while maintaining additional capacity for sudden traffic spikes and infrastructure failures.
