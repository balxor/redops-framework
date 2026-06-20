// TypeScript types mirroring the RedOps Framework API (backend/app/schemas).
// Keep these in sync with the Pydantic schemas. Literal unions match the
// backend's `Literal[...]` definitions so the UI can render fixed option lists.

// ---------------------------------------------------------------------------
// Auth & users
// ---------------------------------------------------------------------------

export type RoleName =
  | "admin"
  | "lead_operator"
  | "operator"
  | "reviewer"
  | "client_viewer";

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface CurrentUser {
  user_id: string;
  email: string;
  full_name: string;
  roles: string[];
  is_active: boolean;
}

export interface UserRead extends CurrentUser {
  created_at: string;
  updated_at: string;
  last_login_at: string | null;
}

export interface UserCreate {
  email: string;
  full_name: string;
  password: string;
  roles: RoleName[];
  is_active: boolean;
}

export interface UserUpdate {
  full_name?: string;
  password?: string;
  roles?: RoleName[];
  is_active?: boolean;
}

// ---------------------------------------------------------------------------
// Projects
// ---------------------------------------------------------------------------

export type ProjectStatus = "draft" | "active" | "paused" | "completed" | "archived";

export type EngagementType =
  | "external_pentest"
  | "internal_pentest"
  | "web_application_pentest"
  | "mobile_application_pentest"
  | "cloud_security_assessment"
  | "red_team"
  | "assumed_breach"
  | "purple_team"
  | "internal_assessment";

export type Metadata = Record<string, string | number | boolean | null>;

export interface ProjectRead {
  project_id: string;
  name: string;
  engagement_type: EngagementType;
  status: ProjectStatus;
  client_name: string | null;
  description: string | null;
  start_date: string | null;
  end_date: string | null;
  timezone: string | null;
  tags: string[];
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  engagement_type: EngagementType;
  status?: ProjectStatus;
  client_name?: string | null;
  description?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  timezone?: string | null;
  tags?: string[];
  metadata?: Metadata;
}

export type ProjectUpdate = Partial<ProjectCreate>;

// ---------------------------------------------------------------------------
// Scopes
// ---------------------------------------------------------------------------

export type ScopeStatus = "draft" | "pending_review" | "approved" | "expired" | "revoked";

export type TargetType =
  | "ip_address"
  | "ip_range"
  | "domain"
  | "subdomain"
  | "url"
  | "cloud_account"
  | "repository"
  | "wireless_network"
  | "application"
  | "api"
  | "identity_tenant"
  | "lab_environment";

export type Environment = "production" | "staging" | "development" | "lab" | "unknown";

export type RestrictedAction =
  | "safe_validation_workflow"
  | "exploit_validation"
  | "credential_exposure_validation"
  | "persistence_validation"
  | "lateral_movement_validation"
  | "egress_telemetry_validation"
  | "external_tool_execution"
  | "production_environment_validation";

export interface Target {
  type: TargetType;
  value: string;
  environment: Environment;
  description?: string | null;
  tags: string[];
}

export interface TestWindow {
  start: string;
  end: string;
  timezone?: string | null;
}

export interface ScopeRead {
  scope_id: string;
  project_id: string;
  status: ScopeStatus;
  allowed_targets: Target[];
  forbidden_targets: Target[];
  test_window: TestWindow;
  rules_of_engagement: string | null;
  restricted_actions: RestrictedAction[];
  approval_required: boolean;
  notes: string | null;
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface ScopeCreate {
  status?: ScopeStatus;
  allowed_targets: Target[];
  forbidden_targets?: Target[];
  test_window: TestWindow;
  rules_of_engagement?: string | null;
  restricted_actions?: RestrictedAction[];
  approval_required?: boolean;
  notes?: string | null;
  metadata?: Metadata;
}

export type ScopeUpdate = Partial<ScopeCreate>;

// ---------------------------------------------------------------------------
// Assets
// ---------------------------------------------------------------------------

export type AssetType = "domain" | "ip_address" | "url" | "application" | "host" | "service" | "other";
export type Criticality = "unknown" | "low" | "medium" | "high" | "critical";

export interface AssetRead {
  asset_id: string;
  project_id: string;
  value: string;
  type: AssetType;
  scope_id: string | null;
  environment: string | null;
  criticality: Criticality;
  tags: string[];
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface AssetCreate {
  value: string;
  type: AssetType;
  scope_id?: string | null;
  environment?: string | null;
  criticality?: Criticality;
  tags?: string[];
  metadata?: Metadata;
}

export type AssetUpdate = Partial<AssetCreate>;

// ---------------------------------------------------------------------------
// Campaigns
// ---------------------------------------------------------------------------

export type CampaignStatus = "draft" | "planned" | "approved" | "active" | "completed" | "cancelled";
export type StepStatus = "planned" | "approved" | "executed" | "blocked" | "skipped" | "detected" | "not_detected";

export interface CampaignStep {
  title: string;
  attack_technique_id?: string | null;
  status: StepStatus;
  approval_required: boolean;
  notes?: string | null;
}

export interface CampaignRead {
  campaign_id: string;
  project_id: string;
  name: string;
  objective: string;
  status: CampaignStatus;
  steps: CampaignStep[];
  tags: string[];
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface CampaignCreate {
  name: string;
  objective: string;
  status?: CampaignStatus;
  steps?: CampaignStep[];
  tags?: string[];
  metadata?: Metadata;
}

export type CampaignUpdate = Partial<CampaignCreate>;

// ---------------------------------------------------------------------------
// Actions
// ---------------------------------------------------------------------------

export type ActionType =
  | "manual_validation"
  | "configuration_review"
  | "recon_note"
  | "scanner_result"
  | "exploit_validation_note"
  | "access_validation_note"
  | "detection_validation_note"
  | "cleanup_note";

export type ActionResult = "unknown" | "planned" | "approved" | "executed" | "skipped" | "failed";
export type DetectionStatus =
  | "unknown"
  | "detected"
  | "not_detected"
  | "blocked"
  | "partially_detected"
  | "not_applicable";

export interface ActionRead {
  action_id: string;
  project_id: string;
  operator_id: string;
  campaign_id: string | null;
  campaign_step_id: string | null;
  asset_id: string | null;
  action_type: ActionType;
  action_summary: string;
  action_detail: string | null;
  result: ActionResult;
  detection_status: DetectionStatus;
  started_at: string | null;
  ended_at: string | null;
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface ActionCreate {
  campaign_id?: string | null;
  campaign_step_id?: string | null;
  asset_id?: string | null;
  action_type: ActionType;
  action_summary: string;
  action_detail?: string | null;
  result?: ActionResult;
  detection_status?: DetectionStatus;
  started_at?: string | null;
  ended_at?: string | null;
  metadata?: Metadata;
}

export type ActionUpdate = Partial<ActionCreate>;

// ---------------------------------------------------------------------------
// Evidence
// ---------------------------------------------------------------------------

export type EvidenceType =
  | "screenshot"
  | "terminal_output"
  | "log_file"
  | "log_excerpt"
  | "http_request_response"
  | "scanner_output"
  | "configuration_export"
  | "siem_alert"
  | "edr_alert"
  | "file_hash"
  | "document"
  | "manual_note"
  | "report_reference"
  | "other";

export interface EvidenceRead {
  evidence_id: string;
  project_id: string;
  uploaded_by: string;
  uploaded_at: string;
  action_id: string | null;
  finding_id: string | null;
  asset_id: string | null;
  evidence_type: EvidenceType;
  file_name: string | null;
  file_size: number | null;
  mime_type: string | null;
  file_hash_sha256: string | null;
  description: string;
  sanitized: boolean;
  captured_at: string | null;
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface EvidenceCreate {
  action_id?: string | null;
  finding_id?: string | null;
  asset_id?: string | null;
  evidence_type: EvidenceType;
  file_name?: string | null;
  file_size?: number | null;
  mime_type?: string | null;
  file_hash_sha256?: string | null;
  description: string;
  sanitized?: boolean;
  captured_at?: string | null;
  metadata?: Metadata;
}

export type EvidenceUpdate = Partial<EvidenceCreate>;

// ---------------------------------------------------------------------------
// Findings
// ---------------------------------------------------------------------------

export type Severity = "informational" | "low" | "medium" | "high" | "critical";
export type FindingStatus = "draft" | "under_review" | "confirmed" | "risk_accepted" | "remediated" | "closed";
export type Likelihood = "unknown" | "low" | "medium" | "high";

export interface AttackMapping {
  technique_id: string;
  tactic?: string | null;
  notes?: string | null;
}

export interface FindingRead {
  finding_id: string;
  project_id: string;
  created_by: string;
  title: string;
  summary: string | null;
  severity: Severity;
  status: FindingStatus;
  affected_assets: string[];
  attack_technique_id: string | null;
  attack_mapping: AttackMapping[];
  evidence_ids: string[];
  impact: string | null;
  likelihood: Likelihood;
  recommendation: string | null;
  reviewed_by: string | null;
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface FindingCreate {
  title: string;
  summary?: string | null;
  severity: Severity;
  status?: FindingStatus;
  affected_assets?: string[];
  attack_technique_id?: string | null;
  attack_mapping?: AttackMapping[];
  evidence_ids?: string[];
  impact?: string | null;
  likelihood?: Likelihood;
  recommendation?: string | null;
  reviewed_by?: string | null;
  metadata?: Metadata;
}

export type FindingUpdate = Partial<FindingCreate>;

// ---------------------------------------------------------------------------
// Reports
// ---------------------------------------------------------------------------

export type ReportStatus = "draft" | "generated" | "under_review" | "approved" | "final" | "archived";
export type ReportFormat = "markdown" | "html" | "pdf" | "docx_later";

export interface ReportSection {
  key: string;
  title: string;
  content?: string | null;
  order: number;
}

export interface ReportRead {
  report_id: string;
  project_id: string;
  title: string;
  version: string;
  status: ReportStatus;
  format: ReportFormat;
  file_path: string | null;
  finding_ids: string[];
  evidence_ids: string[];
  sections: ReportSection[];
  prepared_by: string | null;
  reviewed_by: string | null;
  generated_by: string | null;
  generated_at: string | null;
  published_at: string | null;
  metadata: Metadata;
  created_at: string;
  updated_at: string;
}

export interface ReportCreate {
  title: string;
  version?: string;
  status?: ReportStatus;
  format?: ReportFormat;
  file_path?: string | null;
  finding_ids?: string[];
  evidence_ids?: string[];
  sections?: ReportSection[];
  prepared_by?: string | null;
  reviewed_by?: string | null;
  metadata?: Metadata;
}

export type ReportUpdate = Partial<ReportCreate>;

// ---------------------------------------------------------------------------
// Members, safety, ATT&CK
// ---------------------------------------------------------------------------

export type ProjectRole = "lead_operator" | "operator" | "reviewer" | "client_viewer";

export interface ProjectMemberRead {
  project_member_id: string;
  project_id: string;
  user_id: string;
  project_role: ProjectRole;
  created_at: string;
  updated_at: string;
}

export interface ProjectMemberCreate {
  user_id: string;
  project_role: ProjectRole;
}

export interface SafetySummary {
  project_id: string;
  approved_scope_count: number;
  has_approved_scope: boolean;
  restricted_actions: string[];
}

export interface AttackTechnique {
  technique_id: string;
  name: string;
  tactic_refs: string[];
  platforms: string[];
  source: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  checked_at: string;
}
