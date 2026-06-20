import { createContext, useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import {
  getAccessToken,
  setAccessToken,
  UNAUTHORIZED_EVENT,
} from "@/lib/apiClient";
import { authApi } from "@/api/resources";
import type { CurrentUser } from "@/types";

interface AuthContextValue {
  user: CurrentUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (...roles: string[]) => boolean;
}

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(Boolean(getAccessToken()));

  const logout = useCallback(() => {
    setAccessToken(null);
    setUser(null);
  }, []);

  // Restore the session on first load if a token is persisted.
  useEffect(() => {
    let cancelled = false;
    if (!getAccessToken()) {
      setIsLoading(false);
      return;
    }
    authApi
      .me()
      .then((me) => {
        if (!cancelled) setUser(me);
      })
      .catch(() => {
        if (!cancelled) logout();
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [logout]);

  // Global 401 handler: any request that returns 401 logs the user out.
  useEffect(() => {
    const handler = () => logout();
    window.addEventListener(UNAUTHORIZED_EVENT, handler);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, handler);
  }, [logout]);

  const login = useCallback(async (email: string, password: string) => {
    const token = await authApi.login(email, password);
    setAccessToken(token.access_token);
    const me = await authApi.me();
    setUser(me);
  }, []);

  const hasRole = useCallback(
    (...roles: string[]) => (user ? roles.some((r) => user.roles.includes(r)) : false),
    [user],
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      login,
      logout,
      hasRole,
    }),
    [user, isLoading, login, logout, hasRole],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
