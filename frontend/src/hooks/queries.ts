// TanStack Query hooks for every resource. Query keys are namespaced per
// project so invalidation after a mutation is scoped correctly.

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  actionsApi,
  assetsApi,
  approvalsApi,
  auditApi,
  attackApi,
  campaignsApi,
  detectionGapsApi,
  evidenceApi,
  findingsApi,
  llmTasksApi,
  membersApi,
  projectsApi,
  reportsApi,
  safetyApi,
  scopesApi,
  telemetryApi,
  usersApi,
} from "@/api/resources";
import type {
  AssetCreate,
  ActionCreate,
  ApprovalCreate,
  ApprovalDecision,
  CampaignCreate,
  DetectionGapCreate,
  EvidenceCreate,
  FindingCreate,
  LlmTaskCreate,
  LlmTaskReview,
  ProjectCreate,
  ProjectMemberCreate,
  ProjectUpdate,
  ReportCreate,
  ReportGenerateRequest,
  ScopeCreate,
  TelemetryCreate,
  UserCreate,
} from "@/types";

export const keys = {
  projects: ["projects"] as const,
  project: (id: string) => ["projects", id] as const,
  scopes: (id: string) => ["projects", id, "scopes"] as const,
  assets: (id: string) => ["projects", id, "assets"] as const,
  campaigns: (id: string) => ["projects", id, "campaigns"] as const,
  actions: (id: string) => ["projects", id, "actions"] as const,
  evidence: (id: string) => ["projects", id, "evidence"] as const,
  findings: (id: string) => ["projects", id, "findings"] as const,
  reports: (id: string) => ["projects", id, "reports"] as const,
  members: (id: string) => ["projects", id, "members"] as const,
  safety: (id: string) => ["projects", id, "safety"] as const,
  approvals: (id: string) => ["projects", id, "approvals"] as const,
  audit: (id: string) => ["projects", id, "audit"] as const,
  llmTasks: (id: string) => ["projects", id, "llmTasks"] as const,
  telemetry: (id: string) => ["projects", id, "telemetry"] as const,
  detectionGaps: (id: string) => ["projects", id, "detectionGaps"] as const,
  users: ["users"] as const,
  attack: ["attack", "techniques"] as const,
};

// --- Projects --------------------------------------------------------------

export const useProjects = () =>
  useQuery({ queryKey: keys.projects, queryFn: projectsApi.list });

export const useProject = (projectId: string) =>
  useQuery({ queryKey: keys.project(projectId), queryFn: () => projectsApi.get(projectId) });

export function useCreateProject() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ProjectCreate) => projectsApi.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.projects }),
  });
}

export function useUpdateProject(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ProjectUpdate) => projectsApi.update(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.project(projectId) });
      qc.invalidateQueries({ queryKey: keys.projects });
    },
  });
}

export function useDeleteProject() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (projectId: string) => projectsApi.remove(projectId),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.projects }),
  });
}

// --- Sub-resources (read) --------------------------------------------------

export const useScopes = (projectId: string) =>
  useQuery({ queryKey: keys.scopes(projectId), queryFn: () => scopesApi.list(projectId) });

export const useAssets = (projectId: string) =>
  useQuery({ queryKey: keys.assets(projectId), queryFn: () => assetsApi.list(projectId) });

export const useCampaigns = (projectId: string) =>
  useQuery({ queryKey: keys.campaigns(projectId), queryFn: () => campaignsApi.list(projectId) });

export const useActions = (projectId: string) =>
  useQuery({ queryKey: keys.actions(projectId), queryFn: () => actionsApi.list(projectId) });

export const useEvidence = (projectId: string) =>
  useQuery({ queryKey: keys.evidence(projectId), queryFn: () => evidenceApi.list(projectId) });

export const useFindings = (projectId: string) =>
  useQuery({ queryKey: keys.findings(projectId), queryFn: () => findingsApi.list(projectId) });

export const useReports = (projectId: string) =>
  useQuery({ queryKey: keys.reports(projectId), queryFn: () => reportsApi.list(projectId) });

export const useMembers = (projectId: string) =>
  useQuery({ queryKey: keys.members(projectId), queryFn: () => membersApi.list(projectId) });

export const useSafetySummary = (projectId: string) =>
  useQuery({ queryKey: keys.safety(projectId), queryFn: () => safetyApi.summary(projectId) });

export const useApprovals = (projectId: string) =>
  useQuery({ queryKey: keys.approvals(projectId), queryFn: () => approvalsApi.list(projectId) });

export const useAuditLogs = (projectId: string) =>
  useQuery({ queryKey: keys.audit(projectId), queryFn: () => auditApi.list(projectId) });

export const useLlmTasks = (projectId: string) =>
  useQuery({ queryKey: keys.llmTasks(projectId), queryFn: () => llmTasksApi.list(projectId) });

export const useTelemetry = (projectId: string) =>
  useQuery({ queryKey: keys.telemetry(projectId), queryFn: () => telemetryApi.list(projectId) });

export const useDetectionGaps = (projectId: string) =>
  useQuery({ queryKey: keys.detectionGaps(projectId), queryFn: () => detectionGapsApi.list(projectId) });

// --- Sub-resources (mutate) ------------------------------------------------

export function useCreateScope(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ScopeCreate) => scopesApi.create(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.scopes(projectId) });
      qc.invalidateQueries({ queryKey: keys.safety(projectId) });
    },
  });
}

export function useCreateAsset(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: AssetCreate) => assetsApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.assets(projectId) }),
  });
}

export function useCreateCampaign(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: CampaignCreate) => campaignsApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.campaigns(projectId) }),
  });
}

export function useCreateAction(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ActionCreate) => actionsApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.actions(projectId) }),
  });
}

export function useCreateApproval(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ApprovalCreate) => approvalsApi.create(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.approvals(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useApproveApproval(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ approvalId, body }: { approvalId: string; body: ApprovalDecision }) =>
      approvalsApi.approve(projectId, approvalId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.approvals(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useRejectApproval(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ approvalId, body }: { approvalId: string; body: ApprovalDecision }) =>
      approvalsApi.reject(projectId, approvalId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.approvals(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useCreateLlmTask(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: LlmTaskCreate) => llmTasksApi.create(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.llmTasks(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useAcceptLlmTask(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ taskId, body }: { taskId: string; body: LlmTaskReview }) =>
      llmTasksApi.accept(projectId, taskId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.llmTasks(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useRejectLlmTask(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ taskId, body }: { taskId: string; body: LlmTaskReview }) =>
      llmTasksApi.reject(projectId, taskId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.llmTasks(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useCreateTelemetry(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: TelemetryCreate) => telemetryApi.create(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.telemetry(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useCreateDetectionGap(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: DetectionGapCreate) => detectionGapsApi.create(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.detectionGaps(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useCreateEvidence(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: EvidenceCreate) => evidenceApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.evidence(projectId) }),
  });
}

export function useCreateFinding(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: FindingCreate) => findingsApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.findings(projectId) }),
  });
}

export function useCreateReport(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ReportCreate) => reportsApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.reports(projectId) }),
  });
}

export function useGenerateReport(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ReportGenerateRequest) => reportsApi.generate(projectId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.reports(projectId) });
      qc.invalidateQueries({ queryKey: keys.audit(projectId) });
    },
  });
}

export function useCreateMember(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ProjectMemberCreate) => membersApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.members(projectId) }),
  });
}

// --- Users & ATT&CK --------------------------------------------------------

export const useUsers = () => useQuery({ queryKey: keys.users, queryFn: usersApi.list });

export function useCreateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: UserCreate) => usersApi.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.users }),
  });
}

export const useAttackTechniques = () =>
  useQuery({ queryKey: keys.attack, queryFn: attackApi.techniques });
