import { useState, type FormEvent } from "react";
import { useCreateFinding, useFindings } from "@/hooks/queries";
import { useAuth } from "@/auth/useAuth";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import type { FindingRead, Severity } from "@/types";

const SEVERITIES: Severity[] = ["informational", "low", "medium", "high", "critical"];

export function FindingsTab({ projectId }: { projectId: string }) {
  const query = useFindings(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const [open, setOpen] = useState(false);

  const columns: Column<FindingRead>[] = [
    { header: "Title", render: (f) => <span className="font-medium text-slate-100">{f.title}</span> },
    { header: "Severity", render: (f) => <Badge tone={statusTone(f.severity)}>{humanize(f.severity)}</Badge> },
    { header: "Status", render: (f) => <Badge tone={statusTone(f.status)}>{humanize(f.status)}</Badge> },
    { header: "ATT&CK", render: (f) => f.attack_technique_id || "—" },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        rowKey={(f) => f.finding_id}
        emptyTitle="No findings recorded"
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add finding</Button> : undefined}
      />
      <CreateFindingModal projectId={projectId} open={open} onClose={() => setOpen(false)} />
    </>
  );
}

function CreateFindingModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const create = useCreateFinding(projectId);
  const [title, setTitle] = useState("");
  const [severity, setSeverity] = useState<Severity>("medium");
  const [summary, setSummary] = useState("");
  const [techniqueId, setTechniqueId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        title,
        severity,
        summary: summary || null,
        attack_technique_id: techniqueId || null,
      });
      setTitle("");
      setSummary("");
      setTechniqueId("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add finding.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add finding"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-finding-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-finding-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Title" hint="3–300 characters">
          <Input required minLength={3} value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Reflected XSS on search endpoint" />
        </Field>
        <Field label="Severity">
          <Select value={severity} onChange={(e) => setSeverity(e.target.value as Severity)}>
            {SEVERITIES.map((s) => (
              <option key={s} value={s}>
                {humanize(s)}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="ATT&CK technique ID" hint="Optional, e.g. T1059">
          <Input value={techniqueId} onChange={(e) => setTechniqueId(e.target.value)} placeholder="T1059" />
        </Field>
        <Field label="Summary" hint="Optional">
          <Textarea value={summary} onChange={(e) => setSummary(e.target.value)} placeholder="Short description of the issue." />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
