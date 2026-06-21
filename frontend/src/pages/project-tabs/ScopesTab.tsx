import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useCreateScope, useScopes, useUpdateScope } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDate, humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { ENVIRONMENTS, SCOPE_STATUSES, TARGET_TYPES, toApiDateTime } from "./formOptions";
import type { Environment, ScopeRead, ScopeStatus, TargetType } from "@/types";

export function ScopesTab({ projectId }: { projectId: string }) {
  const query = useScopes(projectId);
  const update = useUpdateScope(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator");
  const canUpdate = canCreate;
  const [open, setOpen] = useState(false);
  const columns: Column<ScopeRead>[] = [
    {
      header: "Status",
      render: (s) =>
        canUpdate ? (
          <Select
            value={s.status}
            disabled={update.isPending}
            onChange={(e) => update.mutate({ scopeId: s.scope_id, body: { status: e.target.value as ScopeStatus } })}
          >
            {SCOPE_STATUSES.map((status) => (
              <option key={status} value={status}>
                {humanize(status)}
              </option>
            ))}
          </Select>
        ) : (
          <Badge tone={statusTone(s.status)}>{humanize(s.status)}</Badge>
        ),
    },
    { header: "Allowed targets", render: (s) => String(s.allowed_targets.length) },
    { header: "Restricted actions", render: (s) => String(s.restricted_actions.length) },
    { header: "Approval", render: (s) => (s.approval_required ? "Required" : "Not required") },
    {
      header: "Window",
      render: (s) => `${formatDate(s.test_window.start)} -> ${formatDate(s.test_window.end)}`,
    },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No scopes defined"
        rowKey={(s) => s.scope_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add scope</Button> : undefined}
      />
      {update.error && <ErrorState error={update.error} />}
      <CreateScopeModal projectId={projectId} open={open} onClose={() => setOpen(false)} />
    </>
  );
}

function CreateScopeModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const create = useCreateScope(projectId);
  const [status, setStatus] = useState<ScopeStatus>("approved");
  const [targetType, setTargetType] = useState<TargetType>("domain");
  const [targetValue, setTargetValue] = useState("");
  const [environment, setEnvironment] = useState<Environment>("lab");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [rules, setRules] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        status,
        allowed_targets: [{ type: targetType, value: targetValue, environment, tags: [] }],
        forbidden_targets: [],
        test_window: { start: toApiDateTime(start), end: toApiDateTime(end), timezone: "Asia/Jakarta" },
        rules_of_engagement: rules || null,
        approval_required: true,
      });
      setTargetValue("");
      setRules("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add scope.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add scope"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-scope-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-scope-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Status">
          <Select value={status} onChange={(e) => setStatus(e.target.value as ScopeStatus)}>
            {SCOPE_STATUSES.map((s) => (
              <option key={s} value={s}>
                {humanize(s)}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Allowed target">
          <Input required value={targetValue} onChange={(e) => setTargetValue(e.target.value)} placeholder="app.example.test" />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Target type">
            <Select value={targetType} onChange={(e) => setTargetType(e.target.value as TargetType)}>
              {TARGET_TYPES.map((t) => (
                <option key={t} value={t}>
                  {humanize(t)}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Environment">
            <Select value={environment} onChange={(e) => setEnvironment(e.target.value as Environment)}>
              {ENVIRONMENTS.map((env) => (
                <option key={env} value={env}>
                  {humanize(env)}
                </option>
              ))}
            </Select>
          </Field>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Window start">
            <Input required type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} />
          </Field>
          <Field label="Window end">
            <Input required type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} />
          </Field>
        </div>
        <Field label="Rules of engagement" hint="Optional">
          <Textarea value={rules} onChange={(e) => setRules(e.target.value)} placeholder="Authorized validation boundaries and notes." />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
