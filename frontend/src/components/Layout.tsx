import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "@/auth/useAuth";

interface NavItem {
  to: string;
  label: string;
  icon: JSX.Element;
  roles?: string[];
}

const icon = (d: string) => (
  <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
    <path strokeLinecap="round" strokeLinejoin="round" d={d} />
  </svg>
);

const NAV: NavItem[] = [
  { to: "/", label: "Dashboard", icon: icon("M4 13h6V4H4v9zm0 7h6v-5H4v5zm10 0h6V11h-6v9zm0-16v5h6V4h-6z") },
  { to: "/projects", label: "Projects", icon: icon("M3 7h7l2 2h9v10a2 2 0 01-2 2H3V7z") },
  { to: "/attack", label: "ATT&CK", icon: icon("M12 3l8 4v5c0 5-3.4 8.9-8 10-4.6-1.1-8-5-8-10V7l8-4z") },
  { to: "/users", label: "Users", icon: icon("M16 14a4 4 0 10-8 0M12 7a3 3 0 100 6 3 3 0 000-6zM4 20a8 8 0 0116 0"), roles: ["admin"] },
];

export function Layout() {
  const { user, logout, hasRole } = useAuth();
  const initials = user?.full_name
    ? user.full_name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase()
    : "?";

  return (
    <div className="flex h-screen overflow-hidden bg-ink-950">
      {/* Sidebar */}
      <aside className="hidden w-60 shrink-0 flex-col border-r border-ink-800 bg-ink-900 md:flex">
        <div className="flex items-center gap-2 px-5 py-4">
          <span className="grid h-8 w-8 place-items-center rounded-md bg-brand-600/20 text-brand-400">
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 3l8 4v5c0 5-3.4 8.9-8 10-4.6-1.1-8-5-8-10V7l8-4z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
            </svg>
          </span>
          <div>
            <p className="text-sm font-semibold text-slate-100">RedOps</p>
            <p className="text-[11px] text-slate-500">Console</p>
          </div>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-2">
          {NAV.filter((item) => !item.roles || hasRole(...item.roles)).map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive ? "bg-ink-700 text-white" : "text-slate-400 hover:bg-ink-800 hover:text-slate-200",
                ].join(" ")
              }
            >
              {item.icon}
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-ink-800 px-3 py-3 text-[11px] text-slate-600">
          Authorized engagements only.
        </div>
      </aside>

      {/* Main */}
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-ink-800 bg-ink-900/80 px-5 py-3 backdrop-blur">
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <span className="md:hidden font-semibold text-slate-200">RedOps</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-slate-200">{user?.full_name}</p>
              <p className="text-[11px] text-slate-500">{user?.roles.join(", ") || "no roles"}</p>
            </div>
            <span className="grid h-9 w-9 place-items-center rounded-full bg-brand-600/20 text-sm font-semibold text-brand-300">
              {initials}
            </span>
            <button
              onClick={logout}
              className="rounded-md border border-ink-700 px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-ink-800"
            >
              Log out
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto px-5 py-6 lg:px-8">
          <div className="mx-auto max-w-6xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
