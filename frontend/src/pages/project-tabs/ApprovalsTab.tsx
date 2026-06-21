import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import {
  useApproveApproval,
  useApprovals,
  useCreateApproval,
  useRejectApproval,
  useRevokeApproval,
} from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDateTime, humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { APPROVAL_ENTITY_TYPES, APPROVAL_RISK_LEVELS } from "./formOptions";
import type { ApprovalEntityType, ApprovalRead, ApprovalRiskLevel } from "@/types";

export function ApprovalsTab({ projectId }: { projectId: string }) {
  const query = useApprovals(projectId);
  const { hasRole } = useAuth();
  const canRequest = hasRole("admin", "lead_operator", "operator");
  const canDecide = hasRole("admin", "lead_operator");
  const approve = useApproveApproval(projectId);
  const reject = useRejectApproval(projectId);
  const revoke = useRevokeApproval(projectId);
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function decide(approvalId: string, decision: "approve" | "reject") {
    setError(null);
    try {
      const mutation = decision === "approve" ? approve : reject;
      await mutation.mutateAsync({ approvalId, body: { decision_note: decision === "approve" ? "Approved in console." : "Rejected in console." } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update approval.");
    }
  }

  async function revokeApproval(approvalId: string) {
    setError(null);
    try {
      await revoke.mutateAsync({ approvalId, body: { decision_note: "Revoked in console." } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to revoke approval.");
    }
  }

  const columns: Column<ApprovalRead>[] = [
    { header: "Status", render: (approval) => <Badge tone={statusTone(approval.status)}>{humanize(approval.status)}</Badge> },
    { header: "Entity", render: (approval) => `${humanize(approval.entity_type)}: ${approval.entity_id}` },
    { header: "Risk", render: (approval) => humanize(approval.risk_level) },
    { header: "Reason", render: (approval) => <span className="font-medium text-slate-100">{approval.reason}</span> },
    { header: "Requested", render: (approval) => formatDateTime(approval.requested_at) },
    {
      header: "Decision",
      render: (approval) =>
        canDecide && approval.status === "pending" ? (
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => decide(approval.approval_id, "approve")} loading={approve.isPending}>
              Approve
            </Button>
            <Button variant="danger" onClick={() => decide(approval.approval_id, "reject")} loading={reject.isPending}>
              Reject
            </Button>
          </div>
        ) : canDecide && approval.status === "approved" ? (
          <Button variant="danger" onClick={() => revokeApproval(approval.approval_id)} loading={revoke.isPending}>
            Revoke
          </Button>
        ) : (
          approval.decided_at ? formatDateTime(approval.decided_at) : "-"
        ),
    },
  ];

  return (
    <>
      {error && <ErrorState error={new Error(error)} />}
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No approvals requested"
        rowKey={(approval) => approval.approval_id}
        toolbar={canRequest ? <Button onClick={() => setOpen(true)}>Request approval</Button> : undefined}
      />
      <CreateApprovalModal projectId={projectId} open={open} onClose={() => setOpen(false)} />
    </>
  );
}

function CreateApprovalModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const create = useCreateApproval(projectId);
  const [entityType, setEntityType] = useState<ApprovalEntityType>("action_type");
  const [entityId, setEntityId] = useState("exploit_validation_note");
  const [riskLevel, setRiskLevel] = useState<ApprovalRiskLevel>("controlled");
  const [reason, setReason] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        entity_type: entityType,
        entity_id: entityId,
        risk_level: riskLevel,
        reason,
      });
      setReason("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to request approval.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Request approval"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-approval-form" loading={create.isPending}>
            Request
          </Button>
        </>
      }
    >
      <form id="create-approval-form" onSubmit={onSubmit} className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Entity type">
            <Select value={entityType} onChange={(e) => setEntityType(e.target.value as ApprovalEntityType)}>
              {APPROVAL_ENTITY_TYPES.map((type) => (
                <option key={type} value={type}>
                  {humanize(type)}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Risk level">
            <Select value={riskLevel} onChange={(e) => setRiskLevel(e.target.value as ApprovalRiskLevel)}>
              {APPROVAL_RISK_LEVELS.map((risk) => (
                <option key={risk} value={risk}>
                  {humanize(risk)}
                </option>
              ))}
            </Select>
          </Field>
        </div>
        <Field label="Entity ID">
          <Input required value={entityId} onChange={(e) => setEntityId(e.target.value)} placeholder="exploit_validation_note or campaign id" />
        </Field>
        <Field label="Reason">
          <Textarea required minLength={3} value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Why this controlled workflow requires approval." />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
