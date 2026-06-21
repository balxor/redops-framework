import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useCreateMember, useMembers, useUsers } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Select } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDate, humanize } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { PROJECT_ROLES } from "./formOptions";
import type { ProjectMemberRead, ProjectRole } from "@/types";

export function MembersTab({ projectId }: { projectId: string }) {
  const query = useMembers(projectId);
  const users = useUsers();
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator");
  const [open, setOpen] = useState(false);
  const columns: Column<ProjectMemberRead>[] = [
    { header: "User ID", render: (m) => <span className="font-mono text-xs text-slate-300">{m.user_id}</span> },
    { header: "Project role", render: (m) => <Badge tone="blue">{humanize(m.project_role)}</Badge> },
    { header: "Added", render: (m) => formatDate(m.created_at) },
  ];

  return (
    <>
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No members"
        rowKey={(m) => m.project_member_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Add member</Button> : undefined}
      />
      <CreateMemberModal projectId={projectId} open={open} onClose={() => setOpen(false)} users={users.data ?? []} />
    </>
  );
}

function CreateMemberModal({
  projectId,
  open,
  onClose,
  users,
}: {
  projectId: string;
  open: boolean;
  onClose: () => void;
  users: Array<{ user_id: string; email: string; full_name: string }>;
}) {
  const create = useCreateMember(projectId);
  const [userId, setUserId] = useState("");
  const [projectRole, setProjectRole] = useState<ProjectRole>("operator");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({ user_id: userId, project_role: projectRole });
      setUserId("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add member.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add member"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-member-form" loading={create.isPending} disabled={!userId}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-member-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="User">
          <Select required value={userId} onChange={(e) => setUserId(e.target.value)}>
            <option value="">Select user</option>
            {users.map((user) => (
              <option key={user.user_id} value={user.user_id}>
                {user.full_name} ({user.email})
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Project role">
          <Select value={projectRole} onChange={(e) => setProjectRole(e.target.value as ProjectRole)}>
            {PROJECT_ROLES.map((role) => (
              <option key={role} value={role}>
                {humanize(role)}
              </option>
            ))}
          </Select>
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
