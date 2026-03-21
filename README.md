
# Project Title

# MediFlow — Real-Time Healthcare Appointment & Triage Platform

MediFlow is a distributed event-driven microservices system that allows patients to book doctor appointments, prioritizes cases using a triage engine, and processes notifications asynchronously.

## Architecture

* FastAPI Microservices
* Apache Kafka Event Bus
* PostgreSQL + TimescaleDB
* Redis Distributed Locks
* MinIO Object Storage
* Prometheus + Grafana Monitoring
* OpenTelemetry Distributed Tracing

## Services

| Service              | Description                         |
| -------------------- | ----------------------------------- |
| API Gateway          | Entry point for all client requests |
| Booking Service      | Handles appointment creation        |
| Triage Engine        | ML-based urgency scoring            |
| Slot Manager         | Prevents double booking             |
| Notification Service | Sends SMS/Email                     |

## Tech Stack

* Python
* FastAPI
* Apache Kafka
* PostgreSQL
* Redis
* Docker
* Prometheus
* Grafana
* OpenTelemetry

## Run Locally

```bash
docker compose up
```
