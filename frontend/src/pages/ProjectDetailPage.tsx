import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  useActions,
  useCampaigns,
  useEvidence,
  useMembers,
  useProject,
  useReports,
  useScopes,
} from "@/hooks/queries";
import { Badge, ErrorState, Loading } from "@/components/ui";
import { humanize, formatDate, formatDateTime, statusTone } from "@/lib/format";
import { OverviewTab } from "./project-tabs/OverviewTab";
import { AssetsTab } from "./project-tabs/AssetsTab";
import { FindingsTab } from "./project-tabs/FindingsTab";
import { SafetyTab } from "./project-tabs/SafetyTab";
import { ResourceTable, type Column } from "./project-tabs/ResourceTable";
import type {
  ActionRead,
  CampaignRead,
  EvidenceRead,
  ProjectMemberRead,
  ReportRead,
  ScopeRead,
} from "@/types";

const TABS = [
  "Overview",
  "Scopes",
  "Assets",
  "Campaigns",
  "Actions",
  "Evidence",
  "Findings",
  "Reports",
  "Members",
  "Safety",
] as const;

type Tab = (typeof TABS)[number];

export function ProjectDetailPage() {
  const { projectId = "" } = useParams();
  const { data: project, isLoading, error } = useProject(projectId);
  const [tab, setTab] = useState<Tab>("Overview");

  if (isLoading) return <Loading />;
  if (error) return <ErrorState error={error} />;
  if (!project) return <ErrorState error={new Error("Project not found")} />;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/projects" className="text-xs text-slate-500 hover:text-slate-300">
          ← Projects
        </Link>
        <div className="mt-1 flex flex-wrap items-center gap-3">
          <h1 className="text-xl font-semibold text-slate-100">{project.name}</h1>
          <Badge tone={statusTone(project.status)}>{humanize(project.status)}</Badge>
        </div>
        <p className="text-sm text-slate-500">
          {humanize(project.engagement_type)}
          {project.client_name ? ` · ${project.client_name}` : ""}
        </p>
      </div>

      <div className="flex gap-1 overflow-x-auto border-b border-ink-700">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={[
              "whitespace-nowrap border-b-2 px-3 py-2 text-sm font-medium transition-colors",
              tab === t
                ? "border-brand-500 text-slate-100"
                : "border-transparent text-slate-400 hover:text-slate-200",
            ].join(" ")}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Overview" && <OverviewTab project={project} />}
      {tab === "Scopes" && <ScopesTab projectId={projectId} />}
      {tab === "Assets" && <AssetsTab projectId={projectId} />}
      {tab === "Campaigns" && <CampaignsTab projectId={projectId} />}
      {tab === "Actions" && <ActionsTab projectId={projectId} />}
      {tab === "Evidence" && <EvidenceTab projectId={projectId} />}
      {tab === "Findings" && <FindingsTab projectId={projectId} />}
      {tab === "Reports" && <ReportsTab projectId={projectId} />}
      {tab === "Members" && <MembersTab projectId={projectId} />}
      {tab === "Safety" && <SafetyTab projectId={projectId} />}
    </div>
  );
}

// --- Read-only tabs built on the generic ResourceTable ---------------------

function ScopesTab({ projectId }: { projectId: string }) {
  const query = useScopes(projectId);
  const columns: Column<ScopeRead>[] = [
    { header: "Status", render: (s) => <Badge tone={statusTone(s.status)}>{humanize(s.status)}</Badge> },
    { header: "Allowed targets", render: (s) => String(s.allowed_targets.length) },
    { header: "Restricted actions", render: (s) => String(s.restricted_actions.length) },
    { header: "Approval", render: (s) => (s.approval_required ? "Required" : "Not required") },
    {
      header: "Window",
      render: (s) => `${formatDate(s.test_window.start)} → ${formatDate(s.test_window.end)}`,
    },
  ];
  return <ResourceTable query={query} columns={columns} emptyTitle="No scopes defined" rowKey={(s) => s.scope_id} />;
}

function CampaignsTab({ projectId }: { projectId: string }) {
  const query = useCampaigns(projectId);
  const columns: Column<CampaignRead>[] = [
    { header: "Name", render: (c) => <span className="font-medium text-slate-100">{c.name}</span> },
    { header: "Status", render: (c) => <Badge tone={statusTone(c.status)}>{humanize(c.status)}</Badge> },
    { header: "Steps", render: (c) => String(c.steps.length) },
    { header: "Objective", render: (c) => <span className="text-slate-400">{c.objective}</span> },
  ];
  return <ResourceTable query={query} columns={columns} emptyTitle="No campaigns yet" rowKey={(c) => c.campaign_id} />;
}

function ActionsTab({ projectId }: { projectId: string }) {
  const query = useActions(projectId);
  const columns: Column<ActionRead>[] = [
    { header: "Summary", render: (a) => <span className="font-medium text-slate-100">{a.action_summary}</span> },
    { header: "Type", render: (a) => humanize(a.action_type) },
    { header: "Result", render: (a) => <Badge tone={statusTone(a.result)}>{humanize(a.result)}</Badge> },
    { header: "Detection", render: (a) => <Badge tone={statusTone(a.detection_status)}>{humanize(a.detection_status)}</Badge> },
  ];
  return <ResourceTable query={query} columns={columns} emptyTitle="No actions logged" rowKey={(a) => a.action_id} />;
}

function EvidenceTab({ projectId }: { projectId: string }) {
  const query = useEvidence(projectId);
  const columns: Column<EvidenceRead>[] = [
    { header: "Description", render: (e) => <span className="font-medium text-slate-100">{e.description}</span> },
    { header: "Type", render: (e) => humanize(e.evidence_type) },
    { header: "Sanitized", render: (e) => (e.sanitized ? <Badge tone="green">Yes</Badge> : <Badge tone="amber">No</Badge>) },
    { header: "Captured", render: (e) => formatDateTime(e.captured_at) },
  ];
  return <ResourceTable query={query} columns={columns} emptyTitle="No evidence stored" rowKey={(e) => e.evidence_id} />;
}

function ReportsTab({ projectId }: { projectId: string }) {
  const query = useReports(projectId);
  const columns: Column<ReportRead>[] = [
    { header: "Title", render: (r) => <span className="font-medium text-slate-100">{r.title}</span> },
    { header: "Version", render: (r) => r.version },
    { header: "Status", render: (r) => <Badge tone={statusTone(r.status)}>{humanize(r.status)}</Badge> },
    { header: "Format", render: (r) => humanize(r.format) },
  ];
  return <ResourceTable query={query} columns={columns} emptyTitle="No reports yet" rowKey={(r) => r.report_id} />;
}

function MembersTab({ projectId }: { projectId: string }) {
  const query = useMembers(projectId);
  const columns: Column<ProjectMemberRead>[] = [
    { header: "User ID", render: (m) => <span className="font-mono text-xs text-slate-300">{m.user_id}</span> },
    { header: "Project role", render: (m) => <Badge tone="blue">{humanize(m.project_role)}</Badge> },
    { header: "Added", render: (m) => formatDate(m.created_at) },
  ];
  return <ResourceTable query={query} columns={columns} emptyTitle="No members" rowKey={(m) => m.project_member_id} />;
}
