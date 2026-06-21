import { useAuditLogs } from "@/hooks/queries";
import { Badge } from "@/components/ui";
import { formatDateTime, humanize } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import type { AuditLogRead } from "@/types";

export function AuditTab({ projectId }: { projectId: string }) {
  const query = useAuditLogs(projectId);
  const columns: Column<AuditLogRead>[] = [
    { header: "Time", render: (event) => formatDateTime(event.created_at) },
    { header: "Action", render: (event) => <Badge tone="blue">{humanize(event.action)}</Badge> },
    { header: "Summary", render: (event) => <span className="font-medium text-slate-100">{event.summary}</span> },
    { header: "Actor", render: (event) => <span className="font-mono text-xs text-slate-300">{event.actor_user_id}</span> },
    { header: "Resource", render: (event) => humanize(event.resource_type) },
  ];

  return <ResourceTable query={query} columns={columns} emptyTitle="No audit events yet" rowKey={(event) => event.audit_log_id} />;
}
