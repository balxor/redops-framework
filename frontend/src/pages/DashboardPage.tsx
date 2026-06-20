import { Link } from "react-router-dom";
import { useProjects } from "@/hooks/queries";
import { useAuth } from "@/auth/useAuth";
import { Badge, Card, CardBody, ErrorState, Loading } from "@/components/ui";
import { humanize, statusTone } from "@/lib/format";
import type { ProjectRead } from "@/types";

function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <Card>
      <CardBody>
        <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
        <p className="mt-1 text-2xl font-semibold text-slate-100">{value}</p>
      </CardBody>
    </Card>
  );
}

export function DashboardPage() {
  const { user } = useAuth();
  const { data: projects, isLoading, error } = useProjects();

  const byStatus = (status: ProjectRead["status"]) =>
    projects?.filter((p) => p.status === status).length ?? 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-100">
          Welcome back, {user?.full_name?.split(" ")[0] ?? "operator"}
        </h1>
        <p className="text-sm text-slate-500">Overview of your authorized engagements.</p>
      </div>

      {isLoading && <Loading />}
      {error && <ErrorState error={error} />}

      {projects && (
        <>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <StatCard label="Total projects" value={projects.length} />
            <StatCard label="Active" value={byStatus("active")} />
            <StatCard label="Draft" value={byStatus("draft")} />
            <StatCard label="Completed" value={byStatus("completed")} />
          </div>

          <Card>
            <div className="border-b border-ink-700 px-5 py-4">
              <h3 className="text-sm font-semibold text-slate-100">Recent projects</h3>
            </div>
            <CardBody className="space-y-2">
              {projects.length === 0 && (
                <p className="py-6 text-center text-sm text-slate-500">
                  No projects yet. Head to <Link to="/projects" className="text-brand-400 hover:underline">Projects</Link> to create one.
                </p>
              )}
              {projects.slice(0, 6).map((p) => (
                <Link
                  key={p.project_id}
                  to={`/projects/${p.project_id}`}
                  className="flex items-center justify-between rounded-lg border border-ink-700 px-4 py-3 hover:border-ink-600 hover:bg-ink-700/40"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-slate-100">{p.name}</p>
                    <p className="truncate text-xs text-slate-500">
                      {humanize(p.engagement_type)}
                      {p.client_name ? ` · ${p.client_name}` : ""}
                    </p>
                  </div>
                  <Badge tone={statusTone(p.status)}>{humanize(p.status)}</Badge>
                </Link>
              ))}
            </CardBody>
          </Card>
        </>
      )}
    </div>
  );
}
