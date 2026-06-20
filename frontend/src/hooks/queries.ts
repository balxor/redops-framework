// TanStack Query hooks for every resource. Query keys are namespaced per
// project so invalidation after a mutation is scoped correctly.

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  actionsApi,
  assetsApi,
  attackApi,
  campaignsApi,
  evidenceApi,
  findingsApi,
  membersApi,
  projectsApi,
  reportsApi,
  safetyApi,
  scopesApi,
  usersApi,
} from "@/api/resources";
import type {
  AssetCreate,
  FindingCreate,
  ProjectCreate,
  ProjectMemberCreate,
  ProjectUpdate,
  ScopeCreate,
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

export function useCreateFinding(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: FindingCreate) => findingsApi.create(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.findings(projectId) }),
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
