// Typed wrappers around every RedOps API endpoint, grouped by resource.
// See docs/API_MAPPING.md for the full endpoint -> function table.

import { api } from "@/lib/apiClient";
import type {
  ActionCreate,
  ActionRead,
  ActionUpdate,
  AssetCreate,
  AssetRead,
  AssetUpdate,
  AttackTechnique,
  CampaignCreate,
  CampaignRead,
  CampaignUpdate,
  CurrentUser,
  EvidenceCreate,
  EvidenceRead,
  EvidenceUpdate,
  FindingCreate,
  FindingRead,
  FindingUpdate,
  HealthStatus,
  ProjectCreate,
  ProjectMemberCreate,
  ProjectMemberRead,
  ProjectRead,
  ProjectUpdate,
  ReportCreate,
  ReportRead,
  ReportUpdate,
  SafetySummary,
  ScopeCreate,
  ScopeRead,
  ScopeUpdate,
  TokenResponse,
  UserCreate,
  UserRead,
  UserUpdate,
} from "@/types";

const p = (projectId: string) => `/projects/${encodeURIComponent(projectId)}`;

export const authApi = {
  login: (email: string, password: string) =>
    api.post<TokenResponse>("/auth/login", { email, password }),
  me: () => api.get<CurrentUser>("/auth/me"),
};

export const healthApi = {
  check: () => api.get<HealthStatus>("/health"),
};

export const usersApi = {
  list: () => api.get<UserRead[]>("/users"),
  get: (userId: string) => api.get<UserRead>(`/users/${userId}`),
  create: (body: UserCreate) => api.post<UserRead>("/users", body),
  update: (userId: string, body: UserUpdate) => api.patch<UserRead>(`/users/${userId}`, body),
};

export const projectsApi = {
  list: () => api.get<ProjectRead[]>("/projects"),
  get: (projectId: string) => api.get<ProjectRead>(p(projectId)),
  create: (body: ProjectCreate) => api.post<ProjectRead>("/projects", body),
  update: (projectId: string, body: ProjectUpdate) => api.patch<ProjectRead>(p(projectId), body),
  remove: (projectId: string) => api.delete<void>(p(projectId)),
};

export const scopesApi = {
  list: (projectId: string) => api.get<ScopeRead[]>(`${p(projectId)}/scopes`),
  create: (projectId: string, body: ScopeCreate) =>
    api.post<ScopeRead>(`${p(projectId)}/scopes`, body),
  update: (projectId: string, scopeId: string, body: ScopeUpdate) =>
    api.patch<ScopeRead>(`${p(projectId)}/scopes/${scopeId}`, body),
  // Note: the backend exposes no DELETE for scopes — revoke via status update.
};

export const assetsApi = {
  list: (projectId: string) => api.get<AssetRead[]>(`${p(projectId)}/assets`),
  create: (projectId: string, body: AssetCreate) =>
    api.post<AssetRead>(`${p(projectId)}/assets`, body),
  update: (projectId: string, assetId: string, body: AssetUpdate) =>
    api.patch<AssetRead>(`${p(projectId)}/assets/${assetId}`, body),
  remove: (projectId: string, assetId: string) =>
    api.delete<void>(`${p(projectId)}/assets/${assetId}`),
};

export const campaignsApi = {
  list: (projectId: string) => api.get<CampaignRead[]>(`${p(projectId)}/campaigns`),
  create: (projectId: string, body: CampaignCreate) =>
    api.post<CampaignRead>(`${p(projectId)}/campaigns`, body),
  update: (projectId: string, campaignId: string, body: CampaignUpdate) =>
    api.patch<CampaignRead>(`${p(projectId)}/campaigns/${campaignId}`, body),
};

export const actionsApi = {
  list: (projectId: string) => api.get<ActionRead[]>(`${p(projectId)}/actions`),
  create: (projectId: string, body: ActionCreate) =>
    api.post<ActionRead>(`${p(projectId)}/actions`, body),
  update: (projectId: string, actionId: string, body: ActionUpdate) =>
    api.patch<ActionRead>(`${p(projectId)}/actions/${actionId}`, body),
};

export const evidenceApi = {
  list: (projectId: string) => api.get<EvidenceRead[]>(`${p(projectId)}/evidence`),
  create: (projectId: string, body: EvidenceCreate) =>
    api.post<EvidenceRead>(`${p(projectId)}/evidence`, body),
  update: (projectId: string, evidenceId: string, body: EvidenceUpdate) =>
    api.patch<EvidenceRead>(`${p(projectId)}/evidence/${evidenceId}`, body),
};

export const findingsApi = {
  list: (projectId: string) => api.get<FindingRead[]>(`${p(projectId)}/findings`),
  create: (projectId: string, body: FindingCreate) =>
    api.post<FindingRead>(`${p(projectId)}/findings`, body),
  update: (projectId: string, findingId: string, body: FindingUpdate) =>
    api.patch<FindingRead>(`${p(projectId)}/findings/${findingId}`, body),
};

export const reportsApi = {
  list: (projectId: string) => api.get<ReportRead[]>(`${p(projectId)}/reports`),
  create: (projectId: string, body: ReportCreate) =>
    api.post<ReportRead>(`${p(projectId)}/reports`, body),
  update: (projectId: string, reportId: string, body: ReportUpdate) =>
    api.patch<ReportRead>(`${p(projectId)}/reports/${reportId}`, body),
};

export const membersApi = {
  list: (projectId: string) => api.get<ProjectMemberRead[]>(`${p(projectId)}/members`),
  create: (projectId: string, body: ProjectMemberCreate) =>
    api.post<ProjectMemberRead>(`${p(projectId)}/members`, body),
  remove: (projectId: string, memberId: string) =>
    api.delete<void>(`${p(projectId)}/members/${memberId}`),
};

export const safetyApi = {
  summary: (projectId: string) => api.get<SafetySummary>(`${p(projectId)}/safety/summary`),
};

export const attackApi = {
  techniques: () => api.get<AttackTechnique[]>("/attack/techniques"),
};
