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

export interface ReportGenerateRequest {
  title?: string;
  format?: ReportFormat;
  include_sections?: string[];
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

export interface AuditLogRead {
  audit_log_id: string;
  project_id: string;
  actor_user_id: string;
  action: string;
  resource_type: string;
  resource_id: string | null;
  summary: string;
  detail: Metadata;
  created_at: string;
}

export type ApprovalStatus = "pending" | "approved" | "rejected" | "revoked" | "expired";
export type ApprovalRiskLevel = "standard" | "controlled" | "sensitive" | "high_risk";
export type ApprovalEntityType = "campaign" | "action_type" | "scope" | "policy_exception";

export interface ApprovalRead {
  approval_id: string;
  project_id: string;
  entity_type: ApprovalEntityType;
  entity_id: string;
  status: ApprovalStatus;
  risk_level: ApprovalRiskLevel;
  reason: string;
  conditions: Metadata;
  requested_by: string;
  decided_by: string | null;
  decision_note: string | null;
  requested_at: string;
  decided_at: string | null;
  expires_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ApprovalCreate {
  entity_type: ApprovalEntityType;
  entity_id: string;
  risk_level?: ApprovalRiskLevel;
  reason: string;
  conditions?: Metadata;
  expires_at?: string | null;
}

export interface ApprovalDecision {
  decision_note?: string | null;
}

export type LlmTaskType =
  | "scope_summary"
  | "attack_mapping_suggestion"
  | "campaign_plan_draft"
  | "policy_review"
  | "evidence_summary"
  | "finding_draft"
  | "remediation_draft"
  | "report_draft"
  | "telemetry_gap_analysis"
  | "cleanup_checklist"
  | "terminology_review";
export type LlmTaskStatus = "under_review" | "accepted" | "rejected" | "archived";

export interface LlmTaskRead {
  llm_task_id: string;
  project_id: string;
  task_type: LlmTaskType;
  entity_type: string | null;
  entity_id: string | null;
  status: LlmTaskStatus;
  input_summary: string;
  output_content: string;
  assumptions: string[];
  limitations: string[];
  requires_review: boolean;
  requested_by: string;
  reviewed_by: string | null;
  review_note: string | null;
  reviewed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface LlmTaskCreate {
  task_type: LlmTaskType;
  entity_type?: string | null;
  entity_id?: string | null;
  input_summary: string;
  output_content: string;
  assumptions?: string[];
  limitations?: string[];
  requires_review?: boolean;
}

export interface LlmTaskReview {
  review_note?: string | null;
}

export type TelemetryDetectionStatus =
  | "unknown"
  | "detected"
  | "not_detected"
  | "blocked"
  | "partially_detected"
  | "not_applicable";
export type DetectionGapType =
  | "missing_telemetry"
  | "incomplete_telemetry"
  | "delayed_telemetry"
  | "low_confidence_signal"
  | "missing_data_source"
  | "missing_detection_rule"
  | "blocked_before_detection"
  | "not_reviewed";
export type DetectionGapStatus = "open" | "under_review" | "accepted" | "resolved" | "closed";

export interface TelemetrySignal {
  name: string;
  description?: string | null;
  data_source?: string | null;
  data_component?: string | null;
  signal?: string | null;
  required: boolean;
}

export interface TelemetryRead {
  telemetry_id: string;
  project_id: string;
  campaign_id: string | null;
  campaign_step_id: string | null;
  action_id: string | null;
  finding_id: string | null;
  asset_id: string | null;
  evidence_id: string | null;
  attack_technique_id: string | null;
  expected_telemetry: TelemetrySignal[];
  observed_telemetry: TelemetrySignal[];
  data_source: string | null;
  detection_status: TelemetryDetectionStatus;
  review_note: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface TelemetryCreate {
  campaign_id?: string | null;
  campaign_step_id?: string | null;
  action_id?: string | null;
  finding_id?: string | null;
  asset_id?: string | null;
  evidence_id?: string | null;
  attack_technique_id?: string | null;
  expected_telemetry?: TelemetrySignal[];
  observed_telemetry?: TelemetrySignal[];
  data_source?: string | null;
  detection_status?: TelemetryDetectionStatus;
  review_note?: string | null;
  reviewed_by?: string | null;
  reviewed_at?: string | null;
}

export type TelemetryUpdate = Partial<TelemetryCreate>;

export interface DetectionGapRead {
  gap_id: string;
  project_id: string;
  telemetry_id: string | null;
  campaign_step_id: string | null;
  finding_id: string | null;
  evidence_id: string | null;
  asset_id: string | null;
  attack_technique_id: string | null;
  gap_type: DetectionGapType;
  summary: string;
  impact: string | null;
  recommendation: string | null;
  status: DetectionGapStatus;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface DetectionGapCreate {
  telemetry_id?: string | null;
  campaign_step_id?: string | null;
  finding_id?: string | null;
  evidence_id?: string | null;
  asset_id?: string | null;
  attack_technique_id?: string | null;
  gap_type: DetectionGapType;
  summary: string;
  impact?: string | null;
  recommendation?: string | null;
  status?: DetectionGapStatus;
}

export type DetectionGapUpdate = Partial<DetectionGapCreate>;

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
