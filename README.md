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

- Support multiple organisations (Tenants)
- Ensure strict data isolation
- Keep data isolated per tenant
- Share infrastructure efficiently and safetly
- Scale cleanly
- Bootstrap and manage system level users security
- Share admin-level visibility without breaking tenant boundaries

TenantCore implements the backend foundation required to support those needs.

---

## Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **PostgreSQL**
- **SQLAlchemy (async)**
- **Alembic**
- **Docker & Docker Compose**
- **JWT authentication**

---

## Project status

### Current phase: **v1 — Foundation**

v1 focuses on building a correct, production-grade backend foundation before adding higher-level features.

### Implemented

## Core Infastructure

- FastAPI application structure
- Versioned API routing (`/api/v1`)
- Application lifespan management
- Database engine and session lifecycle handling
- PostgreSQL integration (Async)
- Alembic migrations
- Base domain models

## Multi-Tenancy

- Tenant domain model
- Tenant scoped database models via mixins
- Strict tenant isolation enforced at the repository layer
- Tenant resolution from authenticated user context

## Authentication & Security

- JWT-based authentication
- Password hashing (bcrypt)
- Tken decoding & validation
- User authentication dependency resolution
- Role based admin checks

## Authentication & Security

- Repository pattern (tenant-scoped & admin-scoped)
- Clear seperation between tenant level access and system/admin level access
- Async repository base classes

## Functional APIs

- Project creation & listing (tenants scoped)
- Admin-only tenants listing
- Admin tenant health inspection
- Health check endpoints

## Admin & Bootstrpping

- One-time bootstrap script for system tenants + admin user
- Explicit seperation of bootstrap logic from runtime API
  Guardrails around admin only functionality

### Recenltly completed

- Tenant resolution refactor using shared dependencies
- Admin tenant management endpoints
- Removal of duplicate tenant resolution logic
- OpenAPI correctness fixes
- Repository consolidation and reuse
- Safe database reset and reseeding workflow
- Bootstrap admin script execution & validation

### Next Phase (v2+) - Hardening and production readiness

- Endpoint-level authorization hardening
- Explicit tenant access validation
- Structured API error responses
- Improved admin observability
- Test coverage (unit + integration)
- Docker & Docker Compose setup
- Environment-based configuration
- Production safety checks

---

## Running locally

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
