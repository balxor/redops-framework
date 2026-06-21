import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import {
  useActions,
  useAssets,
  useCreateTelemetry,
  useEvidence,
  useTelemetry,
} from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDateTime, humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { optionLabel, TELEMETRY_STATUSES } from "./formOptions";
import type { TelemetryDetectionStatus, TelemetryRead } from "@/types";

export function TelemetryTab({ projectId }: { projectId: string }) {
  const query = useTelemetry(projectId);
  const actions = useActions(projectId);
  const assets = useAssets(projectId);
  const evidence = useEvidence(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator", "reviewer");
  const [open, setOpen] = useState(false);
  const columns: Column<TelemetryRead>[] = [
    { header: "Status", render: (row) => <Badge tone={statusTone(row.detection_status)}>{humanize(row.detection_status)}</Badge> },
    { header: "Data source", render: (row) => row.data_source || "-" },
    { header: "Technique", render: (row) => row.attack_technique_id || "-" },
    { header: "Review note", render: (row) => <span className="font-medium text-slate-100">{row.review_note || "-"}</span> },
    { header: "Created", render: (row) => formatDateTime(row.created_at) },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No telemetry reviewed"
        rowKey={(row) => row.telemetry_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add telemetry</Button> : undefined}
      />
      <CreateTelemetryModal
        projectId={projectId}
        open={open}
        onClose={() => setOpen(false)}
        actions={actions.data ?? []}
        assets={assets.data ?? []}
        evidence={evidence.data ?? []}
      />
    </>
  );
}

function CreateTelemetryModal({
  projectId,
  open,
  onClose,
  actions,
  assets,
  evidence,
}: {
  projectId: string;
  open: boolean;
  onClose: () => void;
  actions: Array<{ action_id: string; action_summary: string }>;
  assets: Array<{ asset_id: string; value: string }>;
  evidence: Array<{ evidence_id: string; description: string }>;
}) {
  const create = useCreateTelemetry(projectId);
  const [status, setStatus] = useState<TelemetryDetectionStatus>("unknown");
  const [dataSource, setDataSource] = useState("manual_review");
  const [techniqueId, setTechniqueId] = useState("");
  const [expectedName, setExpectedName] = useState("");
  const [observedName, setObservedName] = useState("");
  const [reviewNote, setReviewNote] = useState("");
  const [actionId, setActionId] = useState("");
  const [assetId, setAssetId] = useState("");
  const [evidenceId, setEvidenceId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        action_id: actionId || null,
        asset_id: assetId || null,
        evidence_id: evidenceId || null,
        attack_technique_id: techniqueId || null,
        data_source: dataSource || null,
        detection_status: status,
        expected_telemetry: expectedName ? [{ name: expectedName, data_source: dataSource || null, required: true }] : [],
        observed_telemetry: observedName ? [{ name: observedName, data_source: dataSource || null, required: false }] : [],
        review_note: reviewNote || null,
      });
      setExpectedName("");
      setObservedName("");
      setReviewNote("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add telemetry.");
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="Add telemetry" footer={<><Button variant="secondary" type="button" onClick={onClose}>Cancel</Button><Button type="submit" form="create-telemetry-form" loading={create.isPending}>Add</Button></>}>
      <form id="create-telemetry-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Detection status">
          <Select value={status} onChange={(e) => setStatus(e.target.value as TelemetryDetectionStatus)}>
            {TELEMETRY_STATUSES.map((item) => <option key={item} value={item}>{humanize(item)}</option>)}
          </Select>
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Data source"><Input value={dataSource} onChange={(e) => setDataSource(e.target.value)} /></Field>
          <Field label="ATT&CK technique" hint="Optional"><Input value={techniqueId} onChange={(e) => setTechniqueId(e.target.value)} placeholder="T1046" /></Field>
        </div>
        <Field label="Expected telemetry" hint="Optional"><Input value={expectedName} onChange={(e) => setExpectedName(e.target.value)} placeholder="Process creation event" /></Field>
        <Field label="Observed telemetry" hint="Optional"><Input value={observedName} onChange={(e) => setObservedName(e.target.value)} placeholder="Endpoint alert observed" /></Field>
        <div className="grid gap-4 sm:grid-cols-3">
          <Field label="Action" hint="Optional">
            <Select value={actionId} onChange={(e) => setActionId(e.target.value)}>
              <option value="">None</option>
              {actions.map((action) => <option key={action.action_id} value={action.action_id}>{optionLabel(action.action_id, action.action_summary)}</option>)}
            </Select>
          </Field>
          <Field label="Asset" hint="Optional">
            <Select value={assetId} onChange={(e) => setAssetId(e.target.value)}>
              <option value="">None</option>
              {assets.map((asset) => <option key={asset.asset_id} value={asset.asset_id}>{optionLabel(asset.asset_id, asset.value)}</option>)}
            </Select>
          </Field>
          <Field label="Evidence" hint="Optional">
            <Select value={evidenceId} onChange={(e) => setEvidenceId(e.target.value)}>
              <option value="">None</option>
              {evidence.map((item) => <option key={item.evidence_id} value={item.evidence_id}>{optionLabel(item.evidence_id, item.description)}</option>)}
            </Select>
          </Field>
        </div>
        <Field label="Review note" hint="Optional"><Textarea value={reviewNote} onChange={(e) => setReviewNote(e.target.value)} /></Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
