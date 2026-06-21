import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useAcceptLlmTask, useCreateLlmTask, useLlmTasks, useRejectLlmTask } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { formatDateTime, humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { LLM_TASK_TYPES } from "./formOptions";
import type { LlmTaskRead, LlmTaskType } from "@/types";

export function LlmDraftsTab({ projectId }: { projectId: string }) {
  const query = useLlmTasks(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const canReview = hasRole("admin", "lead_operator", "reviewer");
  const accept = useAcceptLlmTask(projectId);
  const reject = useRejectLlmTask(projectId);
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function review(taskId: string, decision: "accept" | "reject") {
    setError(null);
    try {
      const mutation = decision === "accept" ? accept : reject;
      await mutation.mutateAsync({
        taskId,
        body: { review_note: decision === "accept" ? "Accepted after human review." : "Rejected after human review." },
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to review draft.");
    }
  }

  const columns: Column<LlmTaskRead>[] = [
    { header: "Status", render: (task) => <Badge tone={statusTone(task.status)}>{humanize(task.status)}</Badge> },
    { header: "Task", render: (task) => humanize(task.task_type) },
    { header: "Draft", render: (task) => <span className="font-medium text-slate-100">{task.output_content.slice(0, 120)}</span> },
    { header: "Created", render: (task) => formatDateTime(task.created_at) },
    {
      header: "Review",
      render: (task) =>
        canReview && task.status === "under_review" ? (
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => review(task.llm_task_id, "accept")} loading={accept.isPending}>
              Accept
            </Button>
            <Button variant="danger" onClick={() => review(task.llm_task_id, "reject")} loading={reject.isPending}>
              Reject
            </Button>
          </div>
        ) : (
          task.reviewed_at ? formatDateTime(task.reviewed_at) : "-"
        ),
    },
  ];

  return (
    <>
      {error && <ErrorState error={new Error(error)} />}
      <ResourceTable
        query={query}
        columns={columns}
        emptyTitle="No LLM-assisted drafts recorded"
        rowKey={(task) => task.llm_task_id}
        toolbar={canCreate ? <Button onClick={() => setOpen(true)}>Record draft</Button> : undefined}
      />
      <CreateLlmDraftModal projectId={projectId} open={open} onClose={() => setOpen(false)} />
    </>
  );
}

function CreateLlmDraftModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const create = useCreateLlmTask(projectId);
  const [taskType, setTaskType] = useState<LlmTaskType>("finding_draft");
  const [entityType, setEntityType] = useState("");
  const [entityId, setEntityId] = useState("");
  const [inputSummary, setInputSummary] = useState("");
  const [outputContent, setOutputContent] = useState("");
  const [limitations, setLimitations] = useState("Draft requires human validation before use.");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        task_type: taskType,
        entity_type: entityType || null,
        entity_id: entityId || null,
        input_summary: inputSummary,
        output_content: outputContent,
        limitations: limitations ? [limitations] : [],
        requires_review: true,
      });
      setInputSummary("");
      setOutputContent("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to record draft.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Record LLM-assisted draft"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-llm-draft-form" loading={create.isPending}>
            Record
          </Button>
        </>
      }
    >
      <form id="create-llm-draft-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Task type">
          <Select value={taskType} onChange={(e) => setTaskType(e.target.value as LlmTaskType)}>
            {LLM_TASK_TYPES.map((type) => (
              <option key={type} value={type}>
                {humanize(type)}
              </option>
            ))}
          </Select>
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Entity type" hint="Optional">
            <Input value={entityType} onChange={(e) => setEntityType(e.target.value)} placeholder="finding, report, campaign" />
          </Field>
          <Field label="Entity ID" hint="Optional">
            <Input value={entityId} onChange={(e) => setEntityId(e.target.value)} placeholder="draft or artifact id" />
          </Field>
        </div>
        <Field label="Input summary">
          <Textarea required minLength={3} value={inputSummary} onChange={(e) => setInputSummary(e.target.value)} placeholder="Sanitized prompt or task summary." />
        </Field>
        <Field label="Draft output">
          <Textarea required minLength={3} value={outputContent} onChange={(e) => setOutputContent(e.target.value)} placeholder="Reviewable draft content." />
        </Field>
        <Field label="Limitation">
          <Input value={limitations} onChange={(e) => setLimitations(e.target.value)} />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
