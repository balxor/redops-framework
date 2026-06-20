import { useState, type FormEvent } from "react";
import { Navigate } from "react-router-dom";
import { useCreateUser, useUsers } from "@/hooks/queries";
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
import { formatDateTime, humanize } from "@/lib/format";
import type { RoleName } from "@/types";

const ROLES: RoleName[] = ["admin", "lead_operator", "operator", "reviewer", "client_viewer"];

export function UsersPage() {
  const { hasRole } = useAuth();
  const { data: users, isLoading, error } = useUsers();
  const [open, setOpen] = useState(false);

  // Backend restricts /users to admins; guard the route client-side too.
  if (!hasRole("admin")) return <Navigate to="/" replace />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-100">Users</h1>
          <p className="text-sm text-slate-500">Manage operator accounts and roles.</p>
        </div>
        <Button onClick={() => setOpen(true)}>New user</Button>
      </div>

      {isLoading && <Loading />}
      {error && <ErrorState error={error} />}
      {users && users.length === 0 && <EmptyState title="No users" />}

      {users && users.length > 0 && (
        <Card>
          <Table>
            <thead>
              <tr>
                <Th>Name</Th>
                <Th>Email</Th>
                <Th>Roles</Th>
                <Th>Active</Th>
                <Th>Last login</Th>
              </tr>
            </thead>
            <tbody className="divide-y divide-ink-800">
              {users.map((u) => (
                <tr key={u.user_id} className="hover:bg-ink-700/30">
                  <Td>
                    <span className="font-medium text-slate-100">{u.full_name}</span>
                  </Td>
                  <Td>{u.email}</Td>
                  <Td>
                    <span className="flex flex-wrap gap-1">
                      {u.roles.map((r) => (
                        <Badge key={r} tone="blue">
                          {humanize(r)}
                        </Badge>
                      ))}
                    </span>
                  </Td>
                  <Td>{u.is_active ? <Badge tone="green">Active</Badge> : <Badge tone="red">Disabled</Badge>}</Td>
                  <Td>{formatDateTime(u.last_login_at)}</Td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card>
      )}

      <CreateUserModal open={open} onClose={() => setOpen(false)} />
    </div>
  );
}

function CreateUserModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const create = useCreateUser();
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<RoleName>("operator");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        email,
        full_name: fullName,
        password,
        roles: [role],
        is_active: true,
      });
      setEmail("");
      setFullName("");
      setPassword("");
      setRole("operator");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create user.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="New user"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-user-form" loading={create.isPending}>
            Create
          </Button>
        </>
      }
    >
      <form id="create-user-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Full name">
          <Input required value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Jane Operator" />
        </Field>
        <Field label="Email">
          <Input required type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="jane@example.com" />
        </Field>
        <Field label="Password" hint="Minimum 8 characters">
          <Input required type="password" minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} />
        </Field>
        <Field label="Role">
          <Select value={role} onChange={(e) => setRole(e.target.value as RoleName)}>
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {humanize(r)}
              </option>
            ))}
          </Select>
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
