import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useActions, useAssets, useCampaigns, useCreateAction } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { ACTION_RESULTS, ACTION_TYPES, DETECTION_STATUSES, optionLabel } from "./formOptions";
import type { ActionRead, ActionResult, ActionType, CampaignRead, DetectionStatus } from "@/types";

export function ActionsTab({ projectId }: { projectId: string }) {
  const query = useActions(projectId);
  const campaigns = useCampaigns(projectId);
  const assets = useAssets(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const [open, setOpen] = useState(false);
  const columns: Column<ActionRead>[] = [
    { header: "Summary", render: (a) => <span className="font-medium text-slate-100">{a.action_summary}</span> },
    { header: "Type", render: (a) => humanize(a.action_type) },
    { header: "Result", render: (a) => <Badge tone={statusTone(a.result)}>{humanize(a.result)}</Badge> },
    { header: "Detection", render: (a) => <Badge tone={statusTone(a.detection_status)}>{humanize(a.detection_status)}</Badge> },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No actions logged"
        rowKey={(a) => a.action_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add action</Button> : undefined}
      />
      <CreateActionModal
        projectId={projectId}
        open={open}
        onClose={() => setOpen(false)}
        campaigns={campaigns.data ?? []}
        assets={assets.data ?? []}
      />
    </>
  );
}

function CreateActionModal({
  projectId,
  open,
  onClose,
  campaigns,
  assets,
}: {
  projectId: string;
  open: boolean;
  onClose: () => void;
  campaigns: CampaignRead[];
  assets: Array<{ asset_id: string; value: string }>;
}) {
  const create = useCreateAction(projectId);
  const [summary, setSummary] = useState("");
  const [detail, setDetail] = useState("");
  const [actionType, setActionType] = useState<ActionType>("manual_validation");
  const [result, setResult] = useState<ActionResult>("unknown");
  const [detection, setDetection] = useState<DetectionStatus>("unknown");
  const [campaignId, setCampaignId] = useState("");
  const [assetId, setAssetId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        action_type: actionType,
        action_summary: summary,
        action_detail: detail || null,
        result,
        detection_status: detection,
        campaign_id: campaignId || null,
        asset_id: assetId || null,
      });
      setSummary("");
      setDetail("");
      setCampaignId("");
      setAssetId("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add action.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add action"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-action-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-action-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Summary">
          <Input required minLength={3} value={summary} onChange={(e) => setSummary(e.target.value)} placeholder="Reviewed endpoint telemetry" />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Type">
            <Select value={actionType} onChange={(e) => setActionType(e.target.value as ActionType)}>
              {ACTION_TYPES.map((t) => (
                <option key={t} value={t}>
                  {humanize(t)}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Result">
            <Select value={result} onChange={(e) => setResult(e.target.value as ActionResult)}>
              {ACTION_RESULTS.map((r) => (
                <option key={r} value={r}>
                  {humanize(r)}
                </option>
              ))}
            </Select>
          </Field>
        </div>
        <Field label="Detection">
          <Select value={detection} onChange={(e) => setDetection(e.target.value as DetectionStatus)}>
            {DETECTION_STATUSES.map((d) => (
              <option key={d} value={d}>
                {humanize(d)}
              </option>
            ))}
          </Select>
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Campaign" hint="Optional">
            <Select value={campaignId} onChange={(e) => setCampaignId(e.target.value)}>
              <option value="">None</option>
              {campaigns.map((campaign) => (
                <option key={campaign.campaign_id} value={campaign.campaign_id}>
                  {optionLabel(campaign.campaign_id, campaign.name)}
                </option>
              ))}
            </Select>
          </Field>
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
        </div>
        <Field label="Detail" hint="Optional">
          <Textarea value={detail} onChange={(e) => setDetail(e.target.value)} placeholder="Manual validation notes and sanitized observations." />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
