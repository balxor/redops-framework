// Thin fetch wrapper for the RedOps API.
//
// - Injects the bearer token from the in-memory token store.
// - Normalises FastAPI error envelopes ({ detail: ... }) into ApiError.
// - Emits an "unauthorized" event on 401 so the auth layer can log out.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, message: string, detail: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

// --- Token store -----------------------------------------------------------
// The token lives in module memory and is mirrored to localStorage so a page
// reload keeps the session. See docs/ARCHITECTURE.md for the security tradeoff.

const TOKEN_STORAGE_KEY = "redops.token";
let accessToken: string | null = readPersistedToken();

function readPersistedToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

export function setAccessToken(token: string | null): void {
  accessToken = token;
  try {
    if (token) localStorage.setItem(TOKEN_STORAGE_KEY, token);
    else localStorage.removeItem(TOKEN_STORAGE_KEY);
  } catch {
    /* storage unavailable (private mode) — session stays in memory only */
  }
}

export function getAccessToken(): string | null {
  return accessToken;
}

// --- Unauthorized signalling ----------------------------------------------

export const UNAUTHORIZED_EVENT = "redops:unauthorized";

function emitUnauthorized(): void {
  window.dispatchEvent(new Event(UNAUTHORIZED_EVENT));
}

// --- Core request ----------------------------------------------------------

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
  body?: unknown;
  signal?: AbortSignal;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, signal } = options;
  const headers: Record<string, string> = { Accept: "application/json" };

  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (accessToken) headers["Authorization"] = `Bearer ${accessToken}`;

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    signal,
  });

  if (response.status === 401) {
    emitUnauthorized();
  }

  if (response.status === 204) {
    return undefined as T;
  }

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json().catch(() => null) : await response.text();

  if (!response.ok) {
    const detail = isJson && payload ? (payload as { detail?: unknown }).detail : payload;
    throw new ApiError(response.status, formatDetail(detail) ?? response.statusText, detail);
  }

  return payload as T;
}

// FastAPI returns `detail` as a string or as a list of validation errors.
function formatDetail(detail: unknown): string | null {
  if (!detail) return null;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === "object" && "msg" in item) {
          const loc = Array.isArray((item as { loc?: unknown[] }).loc)
            ? (item as { loc: unknown[] }).loc.slice(1).join(".")
            : "";
          return loc ? `${loc}: ${(item as { msg: string }).msg}` : (item as { msg: string }).msg;
        }
        return JSON.stringify(item);
      })
      .join("; ");
  }
  return JSON.stringify(detail);
}

export const api = {
  get: <T>(path: string, signal?: AbortSignal) => request<T>(path, { signal }),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: "POST", body }),
  patch: <T>(path: string, body?: unknown) => request<T>(path, { method: "PATCH", body }),
  put: <T>(path: string, body?: unknown) => request<T>(path, { method: "PUT", body }),
  delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
};
