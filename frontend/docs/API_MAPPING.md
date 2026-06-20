# API Mapping

How the frontend talks to the RedOps backend (`backend/app/api/v1`). All paths are
relative to `VITE_API_BASE_URL` (default `/api/v1`). Every request except
`/auth/login` and `/health` requires a bearer token.

## Auth & health

| Method | Path          | Client function     | Hook / usage           |
| ------ | ------------- | ------------------- | ---------------------- |
| POST   | `/auth/login` | `authApi.login`     | `AuthContext.login`    |
| GET    | `/auth/me`    | `authApi.me`        | `AuthContext`          |
| GET    | `/health`     | `healthApi.check`   | (available, unused UI) |

## Users (admin only)

| Method | Path             | Client function    | Hook            |
| ------ | ---------------- | ------------------ | --------------- |
| GET    | `/users`         | `usersApi.list`    | `useUsers`      |
| GET    | `/users/{id}`    | `usersApi.get`     | —               |
| POST   | `/users`         | `usersApi.create`  | `useCreateUser` |
| PATCH  | `/users/{id}`    | `usersApi.update`  | —               |

## Projects

| Method | Path                | Client function     | Hook               |
| ------ | ------------------- | ------------------- | ------------------ |
| GET    | `/projects`         | `projectsApi.list`  | `useProjects`      |
| GET    | `/projects/{id}`    | `projectsApi.get`   | `useProject`       |
| POST   | `/projects`         | `projectsApi.create`| `useCreateProject` |
| PATCH  | `/projects/{id}`    | `projectsApi.update`| `useUpdateProject` |
| DELETE | `/projects/{id}`    | `projectsApi.remove`| `useDeleteProject` |

## Project sub-resources

Base prefix: `/projects/{project_id}`.

| Resource  | GET list | POST create | PATCH update | DELETE | Hooks                                   |
| --------- | -------- | ----------- | ------------ | ------ | --------------------------------------- |
| scopes    | ✅       | ✅          | ✅           | ❌     | `useScopes`, `useCreateScope`           |
| assets    | ✅       | ✅          | ✅           | ✅     | `useAssets`, `useCreateAsset`           |
| campaigns | ✅       | ✅          | ✅           | ❌     | `useCampaigns`                          |
| actions   | ✅       | ✅          | ✅           | ❌     | `useActions`                            |
| evidence  | ✅       | ✅          | ✅           | ❌     | `useEvidence`                           |
| findings  | ✅       | ✅          | ✅           | ❌     | `useFindings`, `useCreateFinding`       |
| reports   | ✅       | ✅          | ✅           | ❌     | `useReports`                            |
| members   | ✅       | ✅          | —            | ✅     | `useMembers`, `useCreateMember`         |
| safety    | `GET /safety/summary` | — | — | —      | `useSafetySummary`                      |

> The DELETE column reflects what the backend actually exposes today. The API
> client only defines `remove()` where a DELETE route exists, so the type system
> prevents calling a non-existent endpoint.

## ATT&CK

| Method | Path                  | Client function       | Hook                  |
| ------ | --------------------- | --------------------- | --------------------- |
| GET    | `/attack/techniques`  | `attackApi.techniques`| `useAttackTechniques` |

## Error envelope

FastAPI returns errors as `{ "detail": ... }` where `detail` is either:

- a **string** (most `HTTPException`s), or
- an **array** of `{ loc, msg, type }` validation errors (422).

`lib/apiClient.ts` normalises both into a single readable message on `ApiError`.

## Auth headers

The client sends `Authorization: Bearer <token>`. The backend reads it via
`OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")`. Note the login endpoint
itself accepts a **JSON** body (`{email, password}`), not OAuth2 form fields.
