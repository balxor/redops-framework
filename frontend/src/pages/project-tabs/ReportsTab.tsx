import { useState, type FormEvent } from "react";
import { useAuth } from "@/auth/useAuth";
import { useCreateReport, useEvidence, useFindings, useGenerateReport, useReports, useUpdateReport } from "@/hooks/queries";
import { Badge, Button, ErrorState, Field, Input, Select, Textarea } from "@/components/ui";
import { Modal } from "@/components/Modal";
import { humanize, statusTone } from "@/lib/format";
import { ResourceTable, type Column } from "./ResourceTable";
import { optionLabel, REPORT_FORMATS, REPORT_STATUSES } from "./formOptions";
import type { ReportFormat, ReportRead, ReportStatus } from "@/types";

export function ReportsTab({ projectId }: { projectId: string }) {
  const query = useReports(projectId);
  const findings = useFindings(projectId);
  const evidence = useEvidence(projectId);
  const update = useUpdateReport(projectId);
  const { hasRole } = useAuth();
  const canCreate = hasRole("admin", "lead_operator", "operator");
  const canReview = hasRole("admin", "lead_operator", "reviewer");
  const [open, setOpen] = useState(false);
  const [generateOpen, setGenerateOpen] = useState(false);
  const columns: Column<ReportRead>[] = [
    { header: "Title", render: (r) => <span className="font-medium text-slate-100">{r.title}</span> },
    { header: "Version", render: (r) => r.version },
    { header: "Status", render: (r) => <Badge tone={statusTone(r.status)}>{humanize(r.status)}</Badge> },
    { header: "Format", render: (r) => humanize(r.format) },
    {
      header: "Status update",
      render: (r) =>
        canReview ? (
          <Select
            aria-label="Report status"
            disabled={update.isPending}
            value={r.status}
            onChange={(e) =>
              update.mutate({
                reportId: r.report_id,
                body: { status: e.target.value as ReportStatus },
              })
            }
          >
            {REPORT_STATUSES.map((status) => (
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
        emptyTitle="No reports yet"
        rowKey={(r) => r.report_id}
        toolbar={
          canCreate ? (
            <div className="flex flex-wrap justify-end gap-2">
              <Button variant="secondary" onClick={() => setGenerateOpen(true)}>
                Generate outline
              </Button>
              <Button onClick={() => setOpen(true)}>Add report</Button>
            </div>
          ) : undefined
        }
      />
      <GenerateReportModal projectId={projectId} open={generateOpen} onClose={() => setGenerateOpen(false)} />
      <CreateReportModal
        projectId={projectId}
        open={open}
        onClose={() => setOpen(false)}
        findings={findings.data ?? []}
        evidence={evidence.data ?? []}
      />
    </>
  );
}

const REPORT_SECTIONS = [
  { key: "executive_summary", label: "Executive summary" },
  { key: "scope", label: "Scope" },
  { key: "campaign_summary", label: "Campaign summary" },
  { key: "action_summary", label: "Action summary" },
  { key: "findings_summary", label: "Findings summary" },
  { key: "evidence_appendix", label: "Evidence appendix" },
  { key: "limitations", label: "Limitations" },
];

function GenerateReportModal({ projectId, open, onClose }: { projectId: string; open: boolean; onClose: () => void }) {
  const generate = useGenerateReport(projectId);
  const [title, setTitle] = useState("Project Report Outline");
  const [format, setFormat] = useState<ReportFormat>("markdown");
  const [sections, setSections] = useState<string[]>(REPORT_SECTIONS.map((section) => section.key));
  const [error, setError] = useState<string | null>(null);

  function toggleSection(sectionKey: string) {
    setSections((current) =>
      current.includes(sectionKey)
        ? current.filter((key) => key !== sectionKey)
        : [...current, sectionKey],
    );
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await generate.mutateAsync({
        title,
        format,
        include_sections: sections,
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate report outline.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Generate report outline"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="generate-report-form" loading={generate.isPending}>
            Generate
          </Button>
        </>
      }
    >
      <form id="generate-report-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Title">
          <Input required minLength={3} value={title} onChange={(e) => setTitle(e.target.value)} />
        </Field>
        <Field label="Format">
          <Select value={format} onChange={(e) => setFormat(e.target.value as ReportFormat)}>
            {REPORT_FORMATS.map((f) => (
              <option key={f} value={f}>
                {humanize(f)}
              </option>
            ))}
          </Select>
        </Field>
        <div className="space-y-2">
          <span className="block text-xs font-medium text-slate-300">Sections</span>
          <div className="grid gap-2 sm:grid-cols-2">
            {REPORT_SECTIONS.map((section) => (
              <label key={section.key} className="flex items-center gap-2 rounded-md border border-ink-700 px-3 py-2 text-sm text-slate-300">
                <input
                  type="checkbox"
                  checked={sections.includes(section.key)}
                  onChange={() => toggleSection(section.key)}
                  className="h-4 w-4 rounded border-ink-600 bg-ink-900"
                />
                {section.label}
              </label>
            ))}
          </div>
        </div>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}

function CreateReportModal({
  projectId,
  open,
  onClose,
  findings,
  evidence,
}: {
  projectId: string;
  open: boolean;
  onClose: () => void;
  findings: Array<{ finding_id: string; title: string }>;
  evidence: Array<{ evidence_id: string; description: string }>;
}) {
  const create = useCreateReport(projectId);
  const [title, setTitle] = useState("");
  const [format, setFormat] = useState<ReportFormat>("markdown");
  const [findingId, setFindingId] = useState("");
  const [evidenceId, setEvidenceId] = useState("");
  const [sectionTitle, setSectionTitle] = useState("Executive Summary");
  const [sectionContent, setSectionContent] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await create.mutateAsync({
        title,
        version: "0.1",
        status: "draft",
        format,
        finding_ids: findingId ? [findingId] : [],
        evidence_ids: evidenceId ? [evidenceId] : [],
        sections: sectionTitle
          ? [
              {
                key: sectionTitle.toLowerCase().replace(/\s+/g, "_"),
                title: sectionTitle,
                content: sectionContent || null,
                order: 1,
              },
            ]
          : [],
      });
      setTitle("");
      setFindingId("");
      setEvidenceId("");
      setSectionContent("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add report.");
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add report"
      footer={
        <>
          <Button variant="secondary" type="button" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="create-report-form" loading={create.isPending}>
            Add
          </Button>
        </>
      }
    >
      <form id="create-report-form" onSubmit={onSubmit} className="space-y-4">
        <Field label="Title">
          <Input required minLength={3} value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Assessment Report" />
        </Field>
        <Field label="Format">
          <Select value={format} onChange={(e) => setFormat(e.target.value as ReportFormat)}>
            {REPORT_FORMATS.map((f) => (
              <option key={f} value={f}>
                {humanize(f)}
              </option>
            ))}
          </Select>
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
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
          <Field label="Evidence" hint="Optional">
            <Select value={evidenceId} onChange={(e) => setEvidenceId(e.target.value)}>
              <option value="">None</option>
              {evidence.map((item) => (
                <option key={item.evidence_id} value={item.evidence_id}>
                  {optionLabel(item.evidence_id, item.description)}
                </option>
              ))}
            </Select>
          </Field>
        </div>
        <Field label="Section title">
          <Input value={sectionTitle} onChange={(e) => setSectionTitle(e.target.value)} />
        </Field>
        <Field label="Section content" hint="Optional">
          <Textarea value={sectionContent} onChange={(e) => setSectionContent(e.target.value)} placeholder="Draft outline or reviewed summary." />
        </Field>
        {error && <ErrorState error={new Error(error)} />}
      </form>
    </Modal>
  );
}
