import { useState, type FormEvent } from "react";
import { useAssets, useCreateAsset } from "@/hooks/queries";
import { useAuth } from "@/auth/useAuth";
import { Badge, Button, ErrorState, Field, Input, Select } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import type { AssetRead, AssetType, Criticality } from "@/types";

const ASSET_TYPES: AssetType[] = ["domain", "ip_address", "url", "application", "host", "service", "other"];
const CRITICALITIES: Criticality[] = ["unknown", "low", "medium", "high", "critical"];

export function AssetsTab({ projectId }: { projectId: string }) {
  const query = useAssets(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const [open, setOpen] = useState(false);

  const columns: Column<AssetRead>[] = [
    { header: "Value", render: (a) => <span className="font-mono text-xs text-slate-100">{a.value}</span> },
    { header: "Type", render: (a) => humanize(a.type) },
    { header: "Criticality", render: (a) => <Badge tone={statusTone(a.criticality)}>{humanize(a.criticality)}</Badge> },
    { header: "Environment", render: (a) => a.environment || "—" },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        rowKey={(a) => a.asset_id}
        emptyTitle="No assets registered"
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add asset</Button> : undefined}
      />
      <CreateAssetModal projectId={projectId} open={open} onClose={() => setOpen(false)} />
    </>
  );
}

function CreateAssetModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const create = useCreateAsset(projectId);
  const [value, setValue] = useState("");
  const [type, setType] = useState<AssetType>("domain");
  const [criticality, setCriticality] = useState<Criticality>("unknown");
  const [environment, setEnvironment] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        value,
        type,
        criticality,
        environment: environment || null,
      });
      setValue("");
      setEnvironment("");
      onClose();
    } catch (err) {
      // The backend rejects assets outside an approved scope (safety gate).
      setError(err instanceof Error ? err.message : "Failed to add asset.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add asset"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-asset-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-asset-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Value" hint="e.g. app.example.com or 10.0.0.5">
          <Input required value={value} onChange={(e) => setValue(e.target.value)} placeholder="app.example.com" />
        </Field>
        <Field label="Type">
          <Select value={type} onChange={(e) => setType(e.target.value as AssetType)}>
            {ASSET_TYPES.map((t) => (
              <option key={t} value={t}>
                {humanize(t)}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Criticality">
          <Select value={criticality} onChange={(e) => setCriticality(e.target.value as Criticality)}>
            {CRITICALITIES.map((c) => (
              <option key={c} value={c}>
                {humanize(c)}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Environment" hint="Optional">
          <Input value={environment} onChange={(e) => setEnvironment(e.target.value)} placeholder="production" />
        </Field>
        <p className="text-xs text-slate-500">
          The backend safety gate rejects assets that fall outside an approved scope target.
        </p>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
