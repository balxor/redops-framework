# Frontend Architecture

This document explains how the RedOps Console is structured and the main design
decisions behind it.

## Goals

- **Robust** — strict TypeScript types mirroring the backend; centralized error
  handling; predictable cache invalidation.
- **Secure** — bearer-token auth with a global 401 handler; server is the source
  of truth for authorization (UI role checks are UX only).
- **Light** — Vite + React, a hand-rolled Tailwind UI kit, and only three runtime
  dependencies (`react`, `react-router-dom`, `@tanstack/react-query`).

## Layered structure

```text
types/                 Plain TS interfaces mirroring backend/app/schemas
  │
lib/apiClient.ts       fetch wrapper: base URL, bearer token, error normalisation
  │
api/resources.ts       One typed function per endpoint, grouped by resource
  │
hooks/queries.ts       TanStack Query hooks + namespaced query keys
  │
pages/ + components/   UI consuming the hooks
```

Each layer depends only on the one above it. A backend change usually means
editing `types/` and `api/resources.ts`; the UI follows.

## Data fetching

[TanStack Query](https://tanstack.com/query) owns all server state. Benefits used
here:

- **Caching** with a 30s `staleTime` to avoid redundant refetches.
- **Retry policy** in `lib/queryClient.ts`: client errors (`status < 500`,
  including 401/403/404/422) are **not** retried; transient 5xx/network errors
  retry twice.
- **Invalidation**: mutations invalidate the affected query keys. Query keys are
  namespaced per project (`["projects", id, "assets"]`) so a mutation only
  refreshes the relevant lists. Creating a scope also invalidates the safety
  summary, since the scope gate depends on it.

There is no global client state library — React context covers auth, and
everything else is server state.

## Authentication & session

Flow:

1. `POST /auth/login` with `{ email, password }` → `{ access_token, ... }`.
2. Token stored via `setAccessToken` (memory + `localStorage`).
3. `GET /auth/me` populates the current user in `AuthContext`.
4. Every request adds `Authorization: Bearer <token>`.
5. On any `401`, `apiClient` dispatches a `redops:unauthorized` window event;
   `AuthContext` listens and logs the user out, sending them to `/login`.

On a hard reload, `AuthProvider` sees a persisted token and re-validates it with
`/auth/me` before rendering protected content (`ProtectedRoute` shows a spinner
during this window).

### Token storage tradeoff

The token lives in `localStorage`, which survives reloads but is readable by any
script running on the page (an XSS risk). This is a deliberate, documented choice
for an internal tool with a trusted operator audience. To harden:

- Move to **httpOnly, Secure, SameSite cookies** issued by the backend, and drop
  the `Authorization` header injection. This requires a backend change (the API
  currently uses the `OAuth2PasswordBearer` header scheme).
- Or keep the token in memory only and accept that reloads require re-login.

The storage logic is isolated in `lib/apiClient.ts`, so switching strategies
touches a single file.

## Authorization

The backend enforces role and project-membership rules on every route. The UI
mirrors a subset (`hasRole`, route guards, conditional buttons) purely to avoid
showing actions that will fail. **Client-side checks are not a security boundary.**

## Styling

Tailwind with a small dark "security console" palette defined in
`tailwind.config.js` (`ink` neutrals + `brand` red). Reusable primitives live in
`components/ui.tsx` (Button, Card, Badge, Table, form fields, states) and
`components/Modal.tsx`. No CSS-in-JS, no component library.

## Error handling

`ApiError` carries the HTTP status and the parsed FastAPI `detail`. The client
flattens FastAPI's validation-error arrays (`[{loc, msg}, ...]`) into a readable
string, so form submissions surface useful messages. Pages render errors with the
shared `ErrorState` component.

## Extending

- **New endpoint**: add the type to `types/`, a function to `api/resources.ts`,
  a hook to `hooks/queries.ts`, then consume it in a page.
- **New sub-resource tab**: most are a `ResourceTable` with a column config; see
  `pages/project-tabs/`. Add a create modal modeled on `AssetsTab`.
