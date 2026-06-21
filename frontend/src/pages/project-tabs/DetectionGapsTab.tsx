import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import {
  useCreateDetectionGap,
  useDetectionGaps,
  useTelemetry,
  useUpdateDetectionGap,
} from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDateTime, humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { DETECTION_GAP_TYPES, optionLabel } from "./formOptions";
import type { DetectionGapRead, DetectionGapType } from "@/types";

export function DetectionGapsTab({ projectId }: { projectId: string }) {
  const query = useDetectionGaps(projectId);
  const telemetry = useTelemetry(projectId);
  const update = useUpdateDetectionGap(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator", "reviewer");
  const canReview = canCreate;
  const [open, setOpen] = useState(false);
  const columns: Column<DetectionGapRead>[] = [
    { header: "Status", render: (gap) => <Badge tone={statusTone(gap.status)}>{humanize(gap.status)}</Badge> },
    { header: "Type", render: (gap) => humanize(gap.gap_type) },
    { header: "Summary", render: (gap) => <span className="font-medium text-slate-100">{gap.summary}</span> },
    { header: "Technique", render: (gap) => gap.attack_technique_id || "-" },
    { header: "Created", render: (gap) => formatDateTime(gap.created_at) },
    {
      header: "Review",
      render: (gap) =>
        canReview && gap.status !== "resolved" && gap.status !== "closed" ? (
          <Button
            variant="secondary"
            loading={update.isPending}
            onClick={() => update.mutate({ gapId: gap.gap_id, body: { status: "resolved" } })}
          >
            Resolve
          </Button>
        ) : (
          "-"
        ),
    },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No detection gaps recorded"
        rowKey={(gap) => gap.gap_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add gap</Button> : undefined}
      />
      <CreateDetectionGapModal projectId={projectId} open={open} onClose={() => setOpen(false)} telemetry={telemetry.data ?? []} />
    </>
  );
}

function CreateDetectionGapModal({
  projectId,
  open,
  onClose,
  telemetry,
}: {
  projectId: string;
  open: boolean;
  onClose: () => void;
  telemetry: Array<{ telemetry_id: string; detection_status: string }>;
}) {
  const create = useCreateDetectionGap(projectId);
  const [gapType, setGapType] = useState<DetectionGapType>("incomplete_telemetry");
  const [summary, setSummary] = useState("");
  const [impact, setImpact] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [techniqueId, setTechniqueId] = useState("");
  const [telemetryId, setTelemetryId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        telemetry_id: telemetryId || null,
        gap_type: gapType,
        summary,
        impact: impact || null,
        recommendation: recommendation || null,
        attack_technique_id: techniqueId || null,
      });
      setSummary("");
      setImpact("");
      setRecommendation("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add detection gap.");
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="Add detection gap" footer={<><Button variant="secondary" type="button" onClick={onClose}>Cancel</Button><Button type="submit" form="create-gap-form" loading={create.isPending}>Add</Button></>}>
      <form id="create-gap-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Gap type">
          <Select value={gapType} onChange={(e) => setGapType(e.target.value as DetectionGapType)}>
            {DETECTION_GAP_TYPES.map((type) => <option key={type} value={type}>{humanize(type)}</option>)}
          </Select>
        </Field>
        <Field label="Telemetry" hint="Optional">
          <Select value={telemetryId} onChange={(e) => setTelemetryId(e.target.value)}>
            <option value="">None</option>
            {telemetry.map((item) => <option key={item.telemetry_id} value={item.telemetry_id}>{optionLabel(item.telemetry_id, humanize(item.detection_status))}</option>)}
          </Select>
        </Field>
        <Field label="ATT&CK technique" hint="Optional"><Input value={techniqueId} onChange={(e) => setTechniqueId(e.target.value)} placeholder="T1046" /></Field>
        <Field label="Summary"><Textarea required minLength={3} value={summary} onChange={(e) => setSummary(e.target.value)} /></Field>
        <Field label="Impact" hint="Optional"><Textarea value={impact} onChange={(e) => setImpact(e.target.value)} /></Field>
        <Field label="Recommendation" hint="Optional"><Textarea value={recommendation} onChange={(e) => setRecommendation(e.target.value)} /></Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
