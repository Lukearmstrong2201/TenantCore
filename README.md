# TenantCore

TenantCore is a backend API project built to explore how modern, multi-tenant SaaS systems are designed and deployed.

The goal of this project is not to build a full product, but to deeply understand real-world backend concepts such as containerisation, authentication, database design, and tenant isolation — the kind of problems you actually run into when building production systems.

This project is being built incrementally, focusing on correctness, structure, and learning rather than speed.

---

## Why this project exists

A lot of tutorials focus on small, isolated examples. TenantCore is different — it is meant to simulate the **core backend of a SaaS platform** that supports multiple organisations (tenants) from a single API.

This gives me a place to:

- Learn Docker properly (not just copy/paste)
- Understand how multi-tenancy works in practice
- Build a clean FastAPI project structure
- Practice authentication, database migrations, and deployment
- Create a portfolio project that reflects real backend work

---

## What problem does it solve?

Many SaaS platforms need to:

- Support multiple organisations
- Keep data isolated per tenant
- Share infrastructure efficiently
- Scale cleanly

TenantCore acts as the foundation for that kind of system.

---

## Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **PostgreSQL** (planned)
- **Docker & Docker Compose** (planned)
- **SQLAlchemy (async)** (planned)
- **JWT authentication** (planned)

---

## Project status

**In active development**

Currently implemented:

- Basic FastAPI application
- Health check endpoint
- Git + SSH authentication setup

Planned next steps:

- Clean project structure
- Environment variable management
- Dockerisation
- Database integration
- Authentication
- Multi-tenant support

---

## Running locally (for now)

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run the API

```bash
uvicorn app.main:app --reload
```

SWAGGER UI visit:

```bash
http://localhost:8000/docs
```
