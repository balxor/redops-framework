import { useState, type FormEvent } from "react";
import { useUpdateProject } from "@/hooks/queries";
import { useAuth } from "@/auth/useAuth";
import { Badge, Button, Card, CardBody, CardHeader, ErrorState, Field, Select } from "@/components/ui";
import { humanize, formatDateTime, statusTone } from "@/lib/format";
import type { ProjectRead, ProjectStatus } from "@/types";

const STATUSES: ProjectStatus[] = ["draft", "active", "paused", "completed", "archived"];

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex justify-between gap-4 py-2 text-sm">
      <span className="text-slate-500">{label}</span>
      <span className="text-right text-slate-200">{children}</span>
    </div>
  );
}

export function OverviewTab({ project }: { project: ProjectRead }) {
  const { hasRole } = useAuth();
  const canEdit = hasRole("admin", "lead_operator");
  const update = useUpdateProject(project.project_id);
  const [status, setStatus] = useState<ProjectStatus>(project.status);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await update.mutateAsync({ status });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Update failed.");
    }
  }

  return (
    <div className="grid gap-4 lg:grid-cols-3">
      <Card className="lg:col-span-2">
        <CardHeader title="Details" />
        <CardBody>
          <div className="divide-y divide-ink-700">
            <Row label="Engagement type">{humanize(project.engagement_type)}</Row>
            <Row label="Status">
              <Badge tone={statusTone(project.status)}>{humanize(project.status)}</Badge>
            </Row>
            <Row label="Client">{project.client_name || "—"}</Row>
            <Row label="Timezone">{project.timezone || "—"}</Row>
            <Row label="Start date">{project.start_date || "—"}</Row>
            <Row label="End date">{project.end_date || "—"}</Row>
            <Row label="Tags">
              {project.tags.length ? (
                <span className="flex flex-wrap justify-end gap-1">
                  {project.tags.map((t) => (
                    <Badge key={t}>{t}</Badge>
                  ))}
                </span>
              ) : (
                "—"
              )}
            </Row>
            <Row label="Created">{formatDateTime(project.created_at)}</Row>
            <Row label="Updated">{formatDateTime(project.updated_at)}</Row>
          </div>
          {project.description && (
            <div className="mt-4 rounded-lg border border-ink-700 bg-ink-900/50 p-3 text-sm text-slate-300">
              {project.description}
            </div>
          )}
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Manage" subtitle={canEdit ? "Update engagement status" : "Read-only"} />
        <CardBody>
          {canEdit ? (
            <form onSubmit={onSubmit} className="space-y-3">
              <Field label="Status">
                <Select value={status} onChange={(e) => setStatus(e.target.value as ProjectStatus)}>
                  {STATUSES.map((s) => (
                    <option key={s} value={s}>
                      {humanize(s)}
                    </option>
                  ))}
                </Select>
              </Field>
              <Button type="submit" loading={update.isPending} disabled={status === project.status} className="w-full">
                Save status
              </Button>
              {error && <ErrorState error={new Error(error)} />}
            </form>
          ) : (
            <p className="text-sm text-slate-500">
              You need the lead_operator or admin role to modify this project.
            </p>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
