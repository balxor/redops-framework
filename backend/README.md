# RedOps Backend

FastAPI backend skeleton for RedOps Framework.

This implementation provides the first API surface for projects, scopes, assets, campaigns, ATT&CK techniques, and health checks.

The application uses SQLAlchemy for persistence and Alembic for database migrations. SQLite is used by default for local development. Docker Compose runs PostgreSQL.

## Run Locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Current Scope

Implemented:

* Health check
* Project CRUD
* Project scope CRUD
* Project asset CRUD
* Campaign CRUD
* ATT&CK technique lookup placeholder
* SQLAlchemy persistence layer
* Alembic initial migration
* Docker Compose PostgreSQL runtime

Not implemented yet:

* Authentication and RBAC
* Evidence file storage
* Report rendering
* External tool integration
* LLM workflow execution
