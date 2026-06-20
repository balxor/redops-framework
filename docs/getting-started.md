# Getting Started

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This guide explains how to run the full RedOps stack locally — the FastAPI
backend, the PostgreSQL database, and the React web console (`frontend/`). For
component-specific details see `backend/README.md` and `frontend/README.md`.

> RedOps is for authorized security work only. The default credentials below are
> for local development and must be changed before any shared or real use.

---

## Prerequisites

| Tool            | Version | Used by            |
| --------------- | ------- | ------------------ |
| Python          | 3.12+   | backend            |
| Node.js         | 18+     | frontend           |
| Docker + Compose| recent  | Option A (compose) |
| PostgreSQL      | 16      | provided by compose|

---

## Option A — Docker Compose (backend + database)

This runs PostgreSQL and the backend together. The frontend still runs via npm
(below), since it is a dev server.

```bash
# from the repo root
docker compose up --build
```

This starts:

- PostgreSQL on `localhost:5432` (db/user/pass: `redops`/`redops`/`redops`)
- Backend on `http://localhost:8000` (runs `alembic upgrade head` first)

Environment comes from `.env.example` (see `docker-compose.yml`). Override values
by copying it to `.env` and editing — **change `REDOPS_JWT_SECRET_KEY` and
`REDOPS_BOOTSTRAP_ADMIN_PASSWORD` before any non-local use.**

Then start the frontend (separate terminal):

```bash
cd frontend
bash dev.sh        # or: npm install && npm run dev
```

Open `http://localhost:5173`.

---

## Option B — Manual (no Docker)

### 1. Backend (SQLite by default)

```bash
cd backend
python -m venv .venv
# Windows:        .venv\Scripts\activate
# Linux/macOS/WSL: source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload      # http://localhost:8000
```

The backend defaults to a local SQLite database, so no PostgreSQL is required
for Option B. To use PostgreSQL instead, set `REDOPS_DATABASE_URL` (see the
configuration table below).

### 2. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev                        # http://localhost:5173
```

The Vite dev server proxies `/api/*` to `http://localhost:8000`, so the browser
talks to a single origin and there is no CORS setup.

---

## Logging in

Default development admin (from `.env.example` / backend config):

```text
Email:    admin@example.com
Password: admin-change-me
```

Change these before sharing the environment. See the security note in the root
`README.md`.

API reference (Swagger UI) is at `http://localhost:8000/docs`.

---

## Key configuration (backend)

Backend settings use the `REDOPS_` env prefix (see `backend/app/core/config.py`):

| Variable                          | Default (dev)                       | Notes                                  |
| --------------------------------- | ----------------------------------- | -------------------------------------- |
| `REDOPS_DATABASE_URL`             | `sqlite:///./redops.db` (compose: PostgreSQL) | Set to a `postgresql+psycopg://...` URL for Postgres |
| `REDOPS_JWT_SECRET_KEY`           | dev placeholder                     | **Must** be changed outside local dev  |
| `REDOPS_BOOTSTRAP_ADMIN_ENABLED`  | `true`                              | Creates the first admin on startup     |
| `REDOPS_BOOTSTRAP_ADMIN_PASSWORD` | `admin-change-me`                   | **Must** be changed outside local dev  |

Frontend settings use the `VITE_` prefix (see `frontend/.env.example`):

| Variable             | Default                 | Notes                                     |
| -------------------- | ----------------------- | ----------------------------------------- |
| `VITE_API_BASE_URL`  | `/api/v1`               | Keep relative to use the dev proxy        |
| `VITE_API_TARGET`    | `http://localhost:8000` | Backend the dev proxy forwards to         |

---

## Ports

| Service     | URL                       |
| ----------- | ------------------------- |
| Frontend    | `http://localhost:5173`   |
| Backend API | `http://localhost:8000`   |
| API docs    | `http://localhost:8000/docs` |
| PostgreSQL  | `localhost:5432`          |

---

## Troubleshooting

- **WSL + project on the Windows drive (`/mnt/c/...`):** hot reload may miss file
  changes. `frontend/dev.sh` auto-detects WSL and enables polling; or set
  `VITE_USE_POLLING=true` manually.
- **`bash dev.sh` permission denied:** run `bash dev.sh` (the executable bit is
  often lost on `/mnt/c` mounts) rather than `./dev.sh`.
- **401 on every request:** the token expired or the backend restarted with a new
  JWT secret — log in again.
- **Frontend loads but API calls fail:** confirm the backend is on `:8000` and
  `VITE_API_TARGET` points to it.
- **`alembic upgrade head` fails on SQLite path:** ensure the working directory is
  writable, or point `REDOPS_DATABASE_URL` at a writable location.

---

## Next steps

- Backend internals and current API scope: `backend/README.md`
- Frontend architecture and extension points: `frontend/README.md`, `frontend/docs/`
- How the system is meant to work: `docs/overview.md`, `docs/product-scope.md`
- Contributor and AI-agent conventions: `CONTRIBUTING.md`, `AGENTS.md`
