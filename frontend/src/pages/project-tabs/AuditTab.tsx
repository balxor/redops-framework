import { useMemo, useState } from "react";
import { useAuditLogs } from "@/hooks/queries";
import { Badge, Input } from "@/components/ui";
import { formatDateTime, humanize } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import type { AuditLogRead } from "@/types";

export function AuditTab({ projectId }: { projectId: string }) {
  const query = useAuditLogs(projectId);
  const [search, setSearch] = useState("");
  const filtered = useMemo(() => {
    const value = search.trim().toLowerCase();
    if (!value) return query.data;
    return query.data?.filter((event) =>
      [
        event.action,
        event.summary,
        event.actor_user_id,
        event.resource_type,
        event.resource_id ?? "",
      ]
        .join(" ")
        .toLowerCase()
        .includes(value),
    );
  }, [query.data, search]);
  const columns: Column<AuditLogRead>[] = [
    { header: "Time", render: (event) => formatDateTime(event.created_at) },
    { header: "Action", render: (event) => <Badge tone="blue">{humanize(event.action)}</Badge> },
    { header: "Summary", render: (event) => <span className="font-medium text-slate-100">{event.summary}</span> },
    { header: "Actor", render: (event) => <span className="font-mono text-xs text-slate-300">{event.actor_user_id}</span> },
    { header: "Resource", render: (event) => humanize(event.resource_type) },
  ];

  return (
    <ResourceTable
      query={query}
      rows={filtered}
      columns={columns}
      emptyTitle={search ? "No matching audit events" : "No audit events yet"}
      rowKey={(event) => event.audit_log_id}
      toolbar={
        <Input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search audit"
          className="w-64"
        />
      }
    />
  );
}
