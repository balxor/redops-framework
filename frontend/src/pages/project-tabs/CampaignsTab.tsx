import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useCampaigns, useCreateCampaign, useUpdateCampaign } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { CAMPAIGN_STATUSES } from "./formOptions";
import type { CampaignRead, CampaignStatus } from "@/types";

export function CampaignsTab({ projectId }: { projectId: string }) {
  const query = useCampaigns(projectId);
  const update = useUpdateCampaign(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator");
  const canUpdate = canCreate;
  const [open, setOpen] = useState(false);
  const columns: Column<CampaignRead>[] = [
    { header: "Name", render: (c) => <span className="font-medium text-slate-100">{c.name}</span> },
    { header: "Status", render: (c) => <Badge tone={statusTone(c.status)}>{humanize(c.status)}</Badge> },
    { header: "Steps", render: (c) => String(c.steps.length) },
    { header: "Objective", render: (c) => <span className="text-slate-400">{c.objective}</span> },
    {
      header: "Status update",
      render: (c) =>
        canUpdate ? (
          <Select
            aria-label="Campaign status"
            disabled={update.isPending}
            value={c.status}
            onChange={(e) =>
              update.mutate({
                campaignId: c.campaign_id,
                body: { status: e.target.value as CampaignStatus },
              })
            }
          >
            {CAMPAIGN_STATUSES.map((status) => (
              <option key={status} value={status}>
                {humanize(status)}
              </option>
            ))}
          </Select>
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
        emptyTitle="No campaigns yet"
        rowKey={(c) => c.campaign_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add campaign</Button> : undefined}
      />
      {update.error && <ErrorState error={update.error} />}
      <CreateCampaignModal projectId={projectId} open={open} onClose={() => setOpen(false)} />
    </>
  );
}

function CreateCampaignModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const create = useCreateCampaign(projectId);
  const [name, setName] = useState("");
  const [objective, setObjective] = useState("");
  const [stepTitle, setStepTitle] = useState("");
  const [techniqueId, setTechniqueId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        name,
        objective,
        status: "draft",
        steps: stepTitle
          ? [
              {
                title: stepTitle,
                attack_technique_id: techniqueId || null,
                status: "planned",
                approval_required: true,
              },
            ]
          : [],
      });
      setName("");
      setObjective("");
      setStepTitle("");
      setTechniqueId("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add campaign.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add campaign"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-campaign-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-campaign-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Name">
          <Input required minLength={3} value={name} onChange={(e) => setName(e.target.value)} placeholder="Discovery validation" />
        </Field>
        <Field label="Objective">
          <Textarea required minLength={3} value={objective} onChange={(e) => setObjective(e.target.value)} placeholder="Validate telemetry for approved discovery activity." />
        </Field>
        <Field label="Initial step" hint="Optional">
          <Input value={stepTitle} onChange={(e) => setStepTitle(e.target.value)} placeholder="Review discovery telemetry" />
        </Field>
        <Field label="ATT&CK technique ID" hint="Optional">
          <Input value={techniqueId} onChange={(e) => setTechniqueId(e.target.value)} placeholder="T1046" />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
