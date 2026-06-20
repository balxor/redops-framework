# RedOps Backend

FastAPI backend skeleton for RedOps Framework.

This implementation provides the first API surface for projects, scopes, assets, campaigns, ATT&CK techniques, and health checks. Data is stored in memory for the initial implementation phase.

## Run Locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
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

Not implemented yet:

* Database persistence
* Alembic migrations
* Authentication and RBAC
* Evidence file storage
* Report rendering
* External tool integration
* LLM workflow execution

