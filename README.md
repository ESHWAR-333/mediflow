# 🏥 MediFlow — Real-Time Healthcare Appointment & Triage Platform

> A **production-grade, event-driven microservices system** simulating how modern healthcare platforms handle appointment booking, AI-powered triage prioritization, distributed slot management, and real-time notifications — all powered by Apache Kafka.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#️-tech-stack)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Services & Ports](#-services--ports)
- [Event Flow](#-event-flow)
- [API Reference](#-api-reference)
- [Monitoring](#-monitoring)
- [What I Learned](#-what-i-learned)
- [Future Improvements](#-future-improvements)

---

## 🔍 Overview

MediFlow simulates a real-world healthcare appointment platform where:

- 🧑‍⚕️ Patients book appointments via a REST API
- ⚡ Events flow asynchronously through **Apache Kafka**
- 🧠 A **triage engine** scores patient urgency in real time
- 🔒 A **slot manager** prevents double-booking using **Redis distributed locks**
- 📩 A **notification service** sends confirmations asynchronously

Each service is fully decoupled, independently deployable, and communicates only through Kafka events — no direct service-to-service calls.

---

## 🏛 Architecture

```
                    ┌─────────────────────────┐
                    │       Client Apps        │
                    │  Patient / Doctor / Admin │
                    └──────────┬──────────────┘
                               │  POST /appointments
                               ▼
                     ┌────────────────────┐
                     │    API Gateway     │  FastAPI :8000
                     └──────────┬─────────┘
                                │  publish
                                ▼
               ┌────────────────────────────────┐
               │         Apache Kafka           │
               │  ┌──────────────────────────┐  │
               │  │    booking.created       │  │
               │  │    triage.scored         │  │
               │  │    slot.updated          │  │
               │  │    notify.send           │  │
               │  └──────────────────────────┘  │
               └────┬──────────┬───────┬────────┘
                    │          │       │
          ┌─────────▼──┐  ┌────▼────┐  └──────────────┐
          │  Booking   │  │ Triage  │                  │
          │  Service   │  │ Engine  │                  │
          │ (Postgres) │  │(Scoring)│                  │
          └────────────┘  └────┬────┘                  │
                               │ triage.scored         │
                               ▼                       ▼
                       ┌──────────────┐    ┌────────────────────┐
                       │ Slot Manager │    │ Notification       │
                       │ (Redis Lock) │    │ Service            │
                       └──────────────┘    └────────────────────┘
```

### Kafka Topic Map

| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `booking.created` | API Gateway | Booking Service, Triage Engine | New appointment request |
| `triage.scored` | Triage Engine | Slot Manager | Urgency scoring result |
| `slot.updated` | Slot Manager | Notification Service | Slot confirmed |
| `notify.send` | Slot Manager | Notification Service | Trigger notification |

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **API** | FastAPI + Uvicorn |
| **Messaging** | Apache Kafka + Zookeeper |
| **Database** | PostgreSQL 15 |
| **Cache / Locking** | Redis 7 |
| **Storage** | MinIO (S3-compatible) |
| **Monitoring** | Prometheus + Grafana |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |
| **Language** | Python 3.11 |

---

## 🔥 Key Features

### ⚡ Event-Driven Architecture
- Fully async, Kafka-based communication between all services
- Zero direct service-to-service HTTP calls — everything flows through topics
- Fault-tolerant: services can restart and resume from Kafka offsets

### 🧠 Triage Engine
- Scores patient urgency based on symptoms in real time
- Keyword-based scoring model (extensible to ML):
  - `chest pain` → urgency **5** (critical)
  - `breathing` → urgency **4**
  - `fever` → urgency **2**
  - default → urgency **1**

### 🔒 Distributed Slot Locking
- Redis `SET NX EX` pattern prevents race conditions
- Guarantees only one booking per `doctor_id + time_slot` combination
- Lock TTL of 30 seconds ensures no permanent deadlocks

### 📩 Async Notification System
- Notification service consumes `slot.updated` events
- Fully decoupled — easy to swap out for email/SMS providers

### 📊 Observability Stack
- **Prometheus** scrapes metrics from all services
- **Grafana** dashboards visualize request rate, latency, and errors
- **Kafka UI** provides real-time topic and consumer group monitoring

---

## 📁 Project Structure

```
mediflow/
│
├── services/
│   ├── api-gateway/               # FastAPI REST API
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routes.py
│   │   │   ├── models.py
│   │   │   ├── producer.py
│   │   │   └── config.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── booking_service/           # Persists bookings to Postgres
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── consumer.py
│   │   │   ├── models.py
│   │   │   ├── db.py
│   │   │   └── config.py
│   │   └── Dockerfile
│   │
│   ├── triage_engine/             # Scores patient urgency
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── consumer.py
│   │   │   ├── producer.py
│   │   │   ├── scoring.py
│   │   │   └── config.py
│   │   └── Dockerfile
│   │
│   ├── slot_manager/              # Redis-based slot locking
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── consumer.py
│   │   │   ├── producer.py
│   │   │   ├── redis_lock.py
│   │   │   └── config.py
│   │   └── Dockerfile
│   │
│   └── notification_service/      # Async notifications
│       ├── app/
│       │   ├── main.py
│       │   ├── consumer.py
│       │   └── config.py
│       └── Dockerfile
│
├── libs/
│   └── kafka_client/              # Shared Kafka producer + event schema
│       ├── producer.py
│       ├── schemas.py
│       └── __init__.py
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose v2+
- 4GB+ RAM recommended (Kafka + all services)

### Run the System

```bash
# Clone the repository
git clone https://github.com/your-username/mediflow.git
cd mediflow

# Start all services
docker compose up --build
```

All services start in dependency order — Zookeeper → Kafka → Databases → Application services. Health checks ensure each dependency is fully ready before dependent services start.

### Verify Everything is Running

```bash
docker ps
```

You should see all containers with status `Up` or `Up (healthy)`.

---

## 🌐 Services & Ports

| Service | URL | Description |
|---------|-----|-------------|
| **API Gateway** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Kafka UI** | http://localhost:8080 | Topic & consumer monitoring |
| **Prometheus** | http://localhost:9090 | Metrics |
| **Grafana** | http://localhost:3000 | Dashboards |
| **MinIO Console** | http://localhost:9001 | Object storage |
| **PostgreSQL** | localhost:5432 | Database |
| **Redis** | localhost:6379 | Cache / locks |

---

## 🔄 Event Flow

```
1. POST /appointments
        │
        ▼
2. API Gateway generates booking_id
   → publishes booking.created to Kafka
        │
        ├──▶ Booking Service
        │    → saves to PostgreSQL
        │
        └──▶ Triage Engine
             → scores urgency from symptoms
             → publishes triage.scored
                    │
                    ▼
             Slot Manager
             → acquires Redis lock on doctor_id + time_slot
             → if lock acquired: publishes slot.updated ✅
             → if already locked: rejects duplicate ❌
                    │
                    ▼
             Notification Service
             → sends confirmation to patient
```

---

## 🧪 API Reference

### Health Check

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

### Book an Appointment

```bash
curl -X POST http://localhost:8000/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT-001",
    "doctor_id": "DOC-001",
    "symptoms": "chest pain",
    "preferred_time": "2026-03-23 10:00"
  }'
```

**Response:**
```json
{
  "booking_id": "3c846d23-332e-4386-842c-43588af3084d",
  "status": "CREATED",
  "message": "Appointment created successfully"
}
```

### Verify Database

```bash
docker exec -it mediflow-postgres psql -U mediflow -d mediflow \
  -c "SELECT * FROM bookings;"
```

### Verify Redis Lock

```bash
docker exec -it mediflow-redis redis-cli keys "*"
# → "DOC-001:2026-03-23 10:00"
```

### Test Duplicate Prevention

Send the same request twice with identical `doctor_id` and `preferred_time` — the slot manager will reject the second booking, confirming the distributed lock works.

---

## 📊 Monitoring

### Prometheus
- Scrapes metrics from all services at `/metrics`
- Tracks: request count, latency histograms, error rates

### Grafana
- Default login: `admin / admin`
- Pre-built dashboards for:
  - Request rate per service
  - P99 latency
  - Kafka consumer lag
  - Active Redis locks

### Kafka UI
- View all topics and their message counts
- Inspect individual events in `booking.created`, `triage.scored`, `slot.updated`
- Monitor consumer group offsets and lag

---

## 🚧 Future Improvements

- [ ] **ML Triage Model** — Replace keyword scoring with a trained classifier
- [ ] **JWT Authentication** — Secure the API Gateway with token-based auth
- [ ] **Kubernetes Deployment** — Helm charts for production-grade orchestration
- [ ] **Alerting** — PagerDuty / Slack alerts for consumer lag and error spikes
- [ ] **Dead Letter Queue** — Handle failed events gracefully
- [ ] **End-to-End Tests** — Automated integration tests across the full event pipeline

---


**Built with ❤️ to demonstrate real-world distributed systems design**

⭐ If you found this useful, give it a star on GitHub!
