# TenantCore

TenantCore is a production-oriented, multi-tenant SaaS backend built with FastAPI and PostgreSQL.

It demonstrates how to design a scalable backend architecture that supports multiple organisations (tenants) from a single API while maintaining strict data isolation, transactional integrity, and role-based access control.

This project focuses on clean architecture, layered design, and production-safe patterns rather than rapid feature delivery.

---

# Overview

Modern SaaS platforms must support:

- Multiple organisations (tenants)
- Strict tenant data isolation
- Role-based access control
- Audit logging
- Admin-level system visibility
- Transactional consistency

TenantCore implements the backend foundation required to support these needs using real-world architectural patterns.

---

# Architecture

TenantCore follows a layered architecture:

API Layer  
→ Handles HTTP concerns, validation, and transaction boundaries

Service Layer  
→ Contains business rules and domain logic

Repository Layer  
→ Handles persistence and tenant-scoped queries

Database  
→ PostgreSQL with async SQLAlchemy

## Key Architectural Decisions

- API-owned transaction management (commit/rollback only in API layer)
- Strict tenant isolation enforced at the repository level
- Role-based project membership enforcement
- Audit logs participate in the same database transaction
- Clear separation between system-admin and tenant-scoped logic
- Async database operations for scalability

This structure mirrors how production SaaS backends are built.

---

# Multi-Tenancy Model

TenantCore enforces isolation using:

- `tenant_id` on all tenant-scoped models
- Repository-level filtering by tenant
- Authenticated user → tenant resolution dependency
- Guardrails preventing cross-tenant data access

No request can access data outside its assigned tenant.

---

# Access Control

Project-level role-based access control is implemented.

Roles:

- OWNER
- MEMBER

Business rules enforced:

- Only project owners can manage members
- A project must always have at least one OWNER
- Cross-tenant access is blocked
- Admin-level routes are explicitly separated from tenant routes

---

# Audit Logging

All membership mutations create audit logs.

Audit logs:

- Are tenant-scoped
- Track actor and target user
- Are written inside the same transaction as the action
- Roll back automatically if the main operation fails

This ensures atomicity and consistency.

---

# Tech Stack

- Python
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic
- JWT Authentication
- bcrypt password hashing
- Docker & Docker Compose

---

# Core Features

## Multi-Tenant Foundation

- Tenant creation (admin-only)
- Tenant-scoped models
- Tenant resolution dependency
- Strict data isolation enforcement

## Authentication & Security

- JWT-based authentication
- Password hashing (bcrypt)
- Role-based admin access
- Dependency-injected current user resolution

## Projects & Membership

- Tenant-scoped project creation
- Project-level membership management
- Owner-only member management
- Protection against removing the last owner

## Audit System

- Mutation logging for project membership
- Actor + target tracking
- Transactionally consistent logging

## Infrastructure

- Async PostgreSQL integration
- Alembic migrations
- Versioned API routing (`/api/v1`)
- Health endpoint (`/api/v1/health`)
- Clean layered structure

---

# Testing

Focused integration tests validate:

- Tenant isolation enforcement
- Project membership permissions
- Prevention of last-owner removal
- Admin-only route protection
- Audit log creation

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
