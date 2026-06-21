import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useProject } from "@/hooks/queries";
import { Badge, ErrorState, Loading } from "@/components/ui";
import { humanize, statusTone } from "@/lib/format";
import { OverviewTab } from "./project-tabs/OverviewTab";
import { ScopesTab } from "./project-tabs/ScopesTab";
import { AssetsTab } from "./project-tabs/AssetsTab";
import { CampaignsTab } from "./project-tabs/CampaignsTab";
import { ActionsTab } from "./project-tabs/ActionsTab";
import { EvidenceTab } from "./project-tabs/EvidenceTab";
import { FindingsTab } from "./project-tabs/FindingsTab";
import { ReportsTab } from "./project-tabs/ReportsTab";
import { MembersTab } from "./project-tabs/MembersTab";
import { SafetyTab } from "./project-tabs/SafetyTab";
import { ApprovalsTab } from "./project-tabs/ApprovalsTab";
import { AuditTab } from "./project-tabs/AuditTab";
import { LlmDraftsTab } from "./project-tabs/LlmDraftsTab";
import { TelemetryTab } from "./project-tabs/TelemetryTab";
import { DetectionGapsTab } from "./project-tabs/DetectionGapsTab";

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
  "Approvals",
  "LLM Drafts",
  "Telemetry",
  "Detection Gaps",
  "Safety",
  "Audit",
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
          &lt;- Projects
        </Link>
        <div className="mt-1 flex flex-wrap items-center gap-3">
          <h1 className="text-xl font-semibold text-slate-100">{project.name}</h1>
          <Badge tone={statusTone(project.status)}>{humanize(project.status)}</Badge>
        </div>
        <p className="text-sm text-slate-500">
          {humanize(project.engagement_type)}
          {project.client_name ? ` - ${project.client_name}` : ""}
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
      {tab === "Approvals" && <ApprovalsTab projectId={projectId} />}
      {tab === "LLM Drafts" && <LlmDraftsTab projectId={projectId} />}
      {tab === "Telemetry" && <TelemetryTab projectId={projectId} />}
      {tab === "Detection Gaps" && <DetectionGapsTab projectId={projectId} />}
      {tab === "Safety" && <SafetyTab projectId={projectId} />}
      {tab === "Audit" && <AuditTab projectId={projectId} />}
    </div>
  );
}
