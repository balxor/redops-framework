import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useActions, useAssets, useCreateEvidence, useEvidence, useFindings, useUpdateEvidence } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDateTime, humanize } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { EVIDENCE_TYPES, optionLabel } from "./formOptions";
import type { ActionRead, EvidenceRead, EvidenceType } from "@/types";

export function EvidenceTab({ projectId }: { projectId: string }) {
  const query = useEvidence(projectId);
  const actions = useActions(projectId);
  const assets = useAssets(projectId);
  const findings = useFindings(projectId);
  const update = useUpdateEvidence(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const canUpdate = canCreate;
  const [open, setOpen] = useState(false);
  const columns: Column<EvidenceRead>[] = [
    { header: "Description", render: (e) => <span className="font-medium text-slate-100">{e.description}</span> },
    { header: "Type", render: (e) => humanize(e.evidence_type) },
    {
      header: "Sanitized",
      render: (e) =>
        canUpdate ? (
          <Select
            value={e.sanitized ? "true" : "false"}
            disabled={update.isPending}
            onChange={(event) =>
              update.mutate({
                evidenceId: e.evidence_id,
                body: { sanitized: event.target.value === "true" },
              })
            }
          >
            <option value="true">Yes</option>
            <option value="false">No</option>
          </Select>
        ) : e.sanitized ? (
          <Badge tone="green">Yes</Badge>
        ) : (
          <Badge tone="amber">No</Badge>
        ),
    },
    { header: "Captured", render: (e) => formatDateTime(e.captured_at) },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No evidence stored"
        rowKey={(e) => e.evidence_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add evidence</Button> : undefined}
      />
      {update.error && <ErrorState error={update.error} />}
      <CreateEvidenceModal
        projectId={projectId}
        open={open}
        onClose={() => setOpen(false)}
        actions={actions.data ?? []}
        assets={assets.data ?? []}
        findings={findings.data ?? []}
      />
    </>
  );
}

function CreateEvidenceModal({
  projectId,
  open,
  onClose,
  actions,
  assets,
  findings,
}: {
  projectId: string;
  open: boolean;
  onClose: () => void;
  actions: ActionRead[];
  assets: Array<{ asset_id: string; value: string }>;
  findings: Array<{ finding_id: string; title: string }>;
}) {
  const create = useCreateEvidence(projectId);
  const [description, setDescription] = useState("");
  const [evidenceType, setEvidenceType] = useState<EvidenceType>("manual_note");
  const [fileName, setFileName] = useState("");
  const [fileHash, setFileHash] = useState("");
  const [sanitized, setSanitized] = useState(true);
  const [actionId, setActionId] = useState("");
  const [assetId, setAssetId] = useState("");
  const [findingId, setFindingId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        description,
        evidence_type: evidenceType,
        file_name: fileName || null,
        file_hash_sha256: fileHash || null,
        sanitized,
        action_id: actionId || null,
        asset_id: assetId || null,
        finding_id: findingId || null,
      });
      setDescription("");
      setFileName("");
      setFileHash("");
      setActionId("");
      setAssetId("");
      setFindingId("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add evidence.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add evidence"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-evidence-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-evidence-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Description">
          <Textarea required minLength={3} value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Sanitized evidence note or file reference." />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Type">
            <Select value={evidenceType} onChange={(e) => setEvidenceType(e.target.value as EvidenceType)}>
              {EVIDENCE_TYPES.map((t) => (
                <option key={t} value={t}>
                  {humanize(t)}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Sanitized">
            <Select value={sanitized ? "true" : "false"} onChange={(e) => setSanitized(e.target.value === "true")}>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </Select>
          </Field>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="File name" hint="Optional">
            <Input value={fileName} onChange={(e) => setFileName(e.target.value)} placeholder="endpoint-alert.txt" />
          </Field>
          <Field label="SHA256" hint="Optional">
            <Input value={fileHash} onChange={(e) => setFileHash(e.target.value)} placeholder="64 hex characters" />
          </Field>
        </div>
        <Field label="Action" hint="Optional">
          <Select value={actionId} onChange={(e) => setActionId(e.target.value)}>
            <option value="">None</option>
            {actions.map((action) => (
              <option key={action.action_id} value={action.action_id}>
                {optionLabel(action.action_id, action.action_summary)}
              </option>
            ))}
          </Select>
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Asset" hint="Optional">
            <Select value={assetId} onChange={(e) => setAssetId(e.target.value)}>
              <option value="">None</option>
              {assets.map((asset) => (
                <option key={asset.asset_id} value={asset.asset_id}>
                  {optionLabel(asset.asset_id, asset.value)}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Finding" hint="Optional">
            <Select value={findingId} onChange={(e) => setFindingId(e.target.value)}>
              <option value="">None</option>
              {findings.map((finding) => (
                <option key={finding.finding_id} value={finding.finding_id}>
                  {optionLabel(finding.finding_id, finding.title)}
                </option>
              ))}
            </Select>
          </Field>
        </div>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
