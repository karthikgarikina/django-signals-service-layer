# Django Signals vs Service Layer

## Overview

This project explores the Django Signals and a Service Layer architecture.

The application manages Orders and User Statistics. It first demonstrates how signals can be used to update statistics automatically, then refactors the same logic into an explicit service layer to improve clarity, testability, and maintainability.

---

## What Was Built

### Models
- Order
- UserStats

### Signals Phase
- Implemented a `post_save` signal for Order creation.
- Updated user statistics automatically.
- Demonstrated common signal pitfalls:
  - Hidden side effects
  - Bulk operations bypassing signals
  - Test isolation challenges

### Service Layer Phase
- Moved business logic into `orders/services.py`
- Added `create_order()` service function.
- Used `transaction.atomic()` for consistency.
- Removed global signal registration from application flow.

### Benchmark
Compared a signal-style approach with an optimized service-layer approach.

Example result:

```text
Signal approach time: 11.87s
Optimized service time: 0.03s
Speedup factor: 312x
```

---

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/karthikgarikina/django-signals-service-layer

cd django-signals-service-layer
```

### 2. Environment Variables

Create a `.env` file from `.env.example`.

Required variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True

POSTGRES_DB=signal_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DB_HOST=db
DB_PORT=5432 
```

---

## Running the Project

### Start with Docker

```bash
docker compose up --build
```

### Stop Containers

```bash
docker compose down
```

---

## Run Tests

```bash
docker compose exec app python manage.py test
```

---

## Run Benchmark

```bash
docker compose exec app python manage.py benchmark_updates
```
---

## Video Demo


---

## Key Takeaway

Signals are useful for event-driven behavior but can introduce hidden side effects and testing complexity. A service layer makes business logic explicit, easier to test, and easier to maintain as applications grow.
