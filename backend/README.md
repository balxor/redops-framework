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

Development login:

```text
Email: admin@example.com
Password: admin-change-me
```

Change these values before using a shared environment.

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
* JWT login
* Bootstrap admin user
* Global role guard for workspace APIs
* Admin user management API
* Project membership API
* Project-level access guard for project resources
* Safety summary API
* Scope allowlist enforcement for assets
* Approved scope requirement for campaign planning
* Action Log API
* Evidence metadata API
* Finding management API
* Report metadata API

Not implemented yet:

* Fine-grained permission matrix
* Evidence file upload and storage
* Report rendering and export
* Report rendering
* External tool integration
* LLM workflow execution
