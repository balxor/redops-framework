# RedOps Console (Frontend)

Web UI for the [RedOps Framework](../README.md) API — an ATT&CK-based platform for managing **authorized** pentest and red team operations.

![Stack](https://img.shields.io/badge/stack-React%2018%20%2B%20Vite%20%2B%20TS-blue)
![Styling](https://img.shields.io/badge/styling-Tailwind%20CSS-38bdf8)
![Data](https://img.shields.io/badge/data-TanStack%20Query-ff4154)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

> This console is for authorized security assessment only. Access requires a valid account on the RedOps backend.

---

## Stack

| Concern         | Choice                          | Why                                                        |
| --------------- | ------------------------------- | ---------------------------------------------------------- |
| Framework       | React 18 + Vite                 | Fast dev server, light build, no SSR overhead for an internal tool |
| Language        | TypeScript (strict)             | Types mirror the backend Pydantic schemas end-to-end       |
| Routing         | React Router v6                 | Nested layout + protected routes                           |
| Server state    | TanStack Query v5               | Caching, retry policy, cache invalidation after mutations  |
| Styling         | Tailwind CSS                    | Small footprint, no component-library lock-in              |
| Auth            | JWT bearer (in-memory + localStorage) | Matches the backend `OAuth2` bearer scheme           |

No backend code is touched by this app — it is a pure API client.

---

## Quick start

Requires **Node.js 18+**.

```bash
cd frontend
cp .env.example .env      # adjust if your API is not on localhost:8000
npm install
npm run dev               # http://localhost:5173
```

The dev server proxies `/api/*` to the backend (default `http://localhost:8000`),
so make sure the API is running:

```bash
# in another terminal, from the repo root
cd backend
uvicorn app.main:app --reload      # http://localhost:8000
```

Log in with the backend's bootstrap admin (see `backend` config — default
`admin@example.com`). **Change those defaults before any real deployment.**

### Scripts

| Command             | Description                              |
| ------------------- | ---------------------------------------- |
| `npm run dev`       | Start the Vite dev server                |
| `npm run build`     | Type-check then build to `dist/`         |
| `npm run preview`   | Preview the production build             |
| `npm run typecheck` | Type-check only (no emit)                |
| `npm run lint`      | ESLint                                   |

---

## Configuration

Environment variables (Vite, prefixed `VITE_`):

| Variable             | Default                 | Purpose                                                |
| -------------------- | ----------------------- | ------------------------------------------------------ |
| `VITE_API_BASE_URL`  | `/api/v1`               | API base. Keep relative to use the dev proxy; set an absolute URL for a separately hosted API. |
| `VITE_API_TARGET`    | `http://localhost:8000` | Backend the dev proxy forwards to (relative base only). |

---

## What's implemented

Aligned with the **current** backend surface (`backend/app/api/v1`).

| Area              | Status | Notes                                                          |
| ----------------- | ------ | -------------------------------------------------------------- |
| Login / session   | ✅ Full | JWT login, `/auth/me` restore, global 401 logout              |
| Dashboard         | ✅ Full | Project counts + recent projects                              |
| Projects          | ✅ CRUD | List, create, detail, status update, delete (per backend)     |
| Project › Overview| ✅ Full | Details + status management                                   |
| Project › Assets  | ✅ List + create | Create respects the backend safety gate              |
| Project › Findings| ✅ List + create |                                                      |
| Project › Scopes / Campaigns / Actions / Evidence / Reports / Members | ✅ List (read) | Create/edit forms are scaffolded via the generic table + hooks and ready to extend |
| Project › Safety  | ✅ Full | Scope-gate summary + restricted actions                       |
| Users (admin)     | ✅ List + create | Admin-only route guard                                |
| ATT&CK            | ✅ List | Reference techniques from `/attack/techniques`                |

> The backend currently exposes `DELETE` only for projects, assets, and members.
> Scopes/campaigns/actions/evidence/findings/reports are create + update only,
> and the API client reflects that (no delete methods for them).

See [`docs/API_MAPPING.md`](./docs/API_MAPPING.md) for the endpoint ↔ function table
and [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) for structure and design decisions.

---

## Project layout

```
frontend/
├── index.html
├── src/
│   ├── api/resources.ts        # typed wrappers for every endpoint
│   ├── auth/                   # AuthContext + useAuth
│   ├── components/             # Layout, ui kit, Modal, ProtectedRoute
│   ├── hooks/queries.ts        # TanStack Query hooks + query keys
│   ├── lib/                    # apiClient, queryClient, formatters
│   ├── pages/                  # route pages (+ project-tabs/)
│   └── types/index.ts          # TS mirror of backend schemas
└── docs/                       # ARCHITECTURE.md, API_MAPPING.md
```

---

## Extending a sub-resource to full CRUD

The read views are generic. To add a create form for, say, campaigns:

1. Add `useCreateCampaign` in `src/hooks/queries.ts` (mirror `useCreateAsset`).
2. Build a modal like `project-tabs/AssetsTab.tsx`.
3. Wire it into the tab's `toolbar` prop.

Types and the API wrapper (`campaignsApi.create`) already exist.

---

## Security notes

- The JWT is held in memory and mirrored to `localStorage` so reloads keep the
  session. This is convenient but readable by injected scripts — see
  `docs/ARCHITECTURE.md` for the tradeoff and how to switch to cookie-based auth.
- Role checks in the UI are **for UX only**. The backend is the source of truth
  for authorization; never rely on client-side role gating for security.
