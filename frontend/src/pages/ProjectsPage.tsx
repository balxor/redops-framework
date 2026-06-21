import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { useCreateProject, useDeleteProject, useProjects, useUpdateProject } from "@/hooks/queries";
import { useAuth } from "@/auth/useAuth";
import {
  Badge,
  Button,
  Card,
  EmptyState,
  ErrorState,
  Field,
  Input,
  Loading,
  Select,
  Table,
  Td,
  Th,
} from "@/components/ui";
import { Modal } from "@/components/Modal";
import { humanize, formatDate, statusTone } from "@/lib/format";
import type { EngagementType, ProjectStatus } from "@/types";

const ENGAGEMENT_TYPES: EngagementType[] = [
  "external_pentest",
  "internal_pentest",
  "web_application_pentest",
  "mobile_application_pentest",
  "cloud_security_assessment",
  "red_team",
  "assumed_breach",
  "purple_team",
  "internal_assessment",
];

const STATUSES: ProjectStatus[] = ["draft", "active", "paused", "completed", "archived"];

export function ProjectsPage() {
  const { data: projects, isLoading, error } = useProjects();
  const deleteProject = useDeleteProject();
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const canEdit = hasRole("admin", "lead_operator");
  const canDelete = hasRole("admin");
  const [open, setOpen] = useState(false);

  function removeProject(project: { project_id: string; name: string }) {
    if (!window.confirm(`Delete project ${project.name}?`)) return;
    deleteProject.mutate(project.project_id);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-100">Projects</h1>
          <p className="text-sm text-slate-500">Engagements you have access to.</p>
        </div>
        {canCreate && <Button onClick={() => setOpen(true)}>New project</Button>}
      </div>

      {isLoading && <Loading />}
      {error && <ErrorState error={error} />}

      {projects && projects.length === 0 && (
        <EmptyState
          title="No projects yet"
          hint="Create your first engagement to start defining scope, assets, and campaigns."
          action={canCreate ? <Button onClick={() => setOpen(true)}>New project</Button> : undefined}
        />
      )}

      {projects && projects.length > 0 && (
        <Card>
          <Table>
            <thead>
              <tr>
                <Th>Name</Th>
                <Th>Type</Th>
                <Th>Client</Th>
                <Th>Status</Th>
                <Th>Updated</Th>
                {canDelete && <Th>Actions</Th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-ink-800">
              {projects.map((p) => (
                <ProjectRow
                  key={p.project_id}
                  project={p}
                  canEdit={canEdit}
                  canDelete={canDelete}
                  deletePending={deleteProject.isPending}
                  onDelete={removeProject}
                />
              ))}
            </tbody>
          </Table>
        </Card>
      )}
      {deleteProject.error && <ErrorState error={deleteProject.error} />}

      <CreateProjectModal open={open} onClose={() => setOpen(false)} />
    </div>
  );
}

function ProjectRow({
  project,
  canEdit,
  canDelete,
  deletePending,
  onDelete,
}: {
  project: { project_id: string; name: string; engagement_type: EngagementType; client_name: string | null; status: ProjectStatus; updated_at: string };
  canEdit: boolean;
  canDelete: boolean;
  deletePending: boolean;
  onDelete: (project: { project_id: string; name: string }) => void;
}) {
  const update = useUpdateProject(project.project_id);

  return (
    <tr className="hover:bg-ink-700/30">
      <Td>
        <Link to={`/projects/${project.project_id}`} className="font-medium text-slate-100 hover:text-brand-400">
          {project.name}
        </Link>
      </Td>
      <Td>{humanize(project.engagement_type)}</Td>
      <Td>{project.client_name || "—"}</Td>
      <Td>
        {canEdit ? (
          <Select
            value={project.status}
            disabled={update.isPending}
            onChange={(e) => update.mutate({ status: e.target.value as ProjectStatus })}
          >
            {STATUSES.map((status) => (
              <option key={status} value={status}>
                {humanize(status)}
              </option>
            ))}
          </Select>
        ) : (
          <Badge tone={statusTone(project.status)}>{humanize(project.status)}</Badge>
        )}
      </Td>
      <Td>{formatDate(project.updated_at)}</Td>
      {canDelete && (
        <Td>
          <Button variant="danger" onClick={() => onDelete(project)} loading={deletePending}>
            Delete
          </Button>
        </Td>
      )}
    </tr>
  );
}

function CreateProjectModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const createProject = useCreateProject();
  const [name, setName] = useState("");
  const [engagementType, setEngagementType] = useState<EngagementType>("external_pentest");
  const [status, setStatus] = useState<ProjectStatus>("draft");
  const [clientName, setClientName] = useState("");
  const [tags, setTags] = useState("");
  const [error, setError] = useState<string | null>(null);

  function reset() {
    setName("");
    setEngagementType("external_pentest");
    setStatus("draft");
    setClientName("");
    setTags("");
    setError(null);
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await createProject.mutateAsync({
        name,
        engagement_type: engagementType,
        status,
        client_name: clientName || null,
        tags: tags ? tags.split(",").map((t) => t.trim()).filter(Boolean) : [],
      });
      reset();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create project.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="New project"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} type="button">
            Cancel
          </Button>
          <Button type="submit" form="create-project-form" loading={createProject.isPending}>
            Create
          </Button>
        </>
      }
    >
      <form id="create-project-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Name" hint="3–200 characters">
          <Input required minLength={3} value={name} onChange={(e) => setName(e.target.value)} placeholder="Acme Q3 external pentest" />
        </Field>
        <Field label="Engagement type">
          <Select value={engagementType} onChange={(e) => setEngagementType(e.target.value as EngagementType)}>
            {ENGAGEMENT_TYPES.map((t) => (
              <option key={t} value={t}>
                {humanize(t)}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Status">
          <Select value={status} onChange={(e) => setStatus(e.target.value as ProjectStatus)}>
            {STATUSES.map((s) => (
              <option key={s} value={s}>
                {humanize(s)}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Client name" hint="Optional">
          <Input value={clientName} onChange={(e) => setClientName(e.target.value)} placeholder="Acme Corp" />
        </Field>
        <Field label="Tags" hint="Comma-separated, optional">
          <Input value={tags} onChange={(e) => setTags(e.target.value)} placeholder="external, web, 2026-q3" />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
