# Monitoring Results – Grafana & Prometheus

This folder documents the monitoring and alerting results of the FastAPI application.

## Dashboard
A Grafana dashboard was used to visualize:
- Request Rate
- FastAPI Failure Rate (HTTP 4xx/5xx)
- Response Time (p50 / p95)
- CPU and Memory Usage

## Stress & Error Simulation
The following endpoints were triggered repeatedly to simulate load and errors:
- POST /concerts/new
- POST /buy/{invalid_id}
- GET non-existing endpoints (404)

## Observations
- Request rate increased during load tests
- Failure rate increased significantly when invalid requests were sent
- Latency showed small spikes under load
- CPU usage fluctuated as expected

## Alerting
An alert rule was configured in Grafana:
- Condition: Failure rate > 2%
- Evaluation interval: 1 minute
- Alert successfully transitioned to **FIRING** state

## Evidence
Screenshots in the `screenshots/` folder show:
- Normal operation
- Increased failure rate
- Alert firing state

