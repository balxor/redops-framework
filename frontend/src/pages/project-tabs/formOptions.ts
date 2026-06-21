import type {
  ActionResult,
  ActionType,
  ApprovalEntityType,
  ApprovalRiskLevel,
  DetectionStatus,
  DetectionGapStatus,
  DetectionGapType,
  Environment,
  EvidenceType,
  FindingStatus,
  LlmTaskType,
  ProjectRole,
  ReportFormat,
  ReportStatus,
  ScopeStatus,
  TargetType,
  TelemetryDetectionStatus,
} from "@/types";

export const SCOPE_STATUSES: ScopeStatus[] = ["draft", "pending_review", "approved", "expired", "revoked"];

export const TARGET_TYPES: TargetType[] = [
  "domain",
  "subdomain",
  "url",
  "ip_address",
  "ip_range",
  "application",
  "api",
  "lab_environment",
];

export const ENVIRONMENTS: Environment[] = ["lab", "development", "staging", "production", "unknown"];

export const ACTION_TYPES: ActionType[] = [
  "manual_validation",
  "configuration_review",
  "recon_note",
  "scanner_result",
  "access_validation_note",
  "detection_validation_note",
  "cleanup_note",
];

export const ACTION_RESULTS: ActionResult[] = ["unknown", "planned", "approved", "executed", "skipped", "failed"];

export const DETECTION_STATUSES: DetectionStatus[] = [
  "unknown",
  "detected",
  "not_detected",
  "blocked",
  "partially_detected",
  "not_applicable",
];

export const EVIDENCE_TYPES: EvidenceType[] = [
  "manual_note",
  "screenshot",
  "log_file",
  "scanner_output",
  "siem_alert",
  "edr_alert",
  "document",
  "other",
];

export const FINDING_STATUSES: FindingStatus[] = [
  "draft",
  "under_review",
  "confirmed",
  "risk_accepted",
  "remediated",
  "closed",
];

export const REPORT_FORMATS: ReportFormat[] = ["markdown", "html", "pdf"];

export const REPORT_STATUSES: ReportStatus[] = [
  "draft",
  "generated",
  "under_review",
  "approved",
  "final",
  "archived",
];

export const PROJECT_ROLES: ProjectRole[] = ["lead_operator", "operator", "reviewer", "client_viewer"];

export const APPROVAL_ENTITY_TYPES: ApprovalEntityType[] = ["campaign", "action_type", "scope", "policy_exception"];

export const APPROVAL_RISK_LEVELS: ApprovalRiskLevel[] = ["standard", "controlled", "sensitive", "high_risk"];

export const LLM_TASK_TYPES: LlmTaskType[] = [
  "scope_summary",
  "attack_mapping_suggestion",
  "campaign_plan_draft",
  "policy_review",
  "evidence_summary",
  "finding_draft",
  "remediation_draft",
  "report_draft",
  "telemetry_gap_analysis",
  "cleanup_checklist",
  "terminology_review",
];

export const TELEMETRY_STATUSES: TelemetryDetectionStatus[] = [
  "unknown",
  "detected",
  "not_detected",
  "blocked",
  "partially_detected",
  "not_applicable",
];

export const DETECTION_GAP_TYPES: DetectionGapType[] = [
  "missing_telemetry",
  "incomplete_telemetry",
  "delayed_telemetry",
  "low_confidence_signal",
  "missing_data_source",
  "missing_detection_rule",
  "blocked_before_detection",
  "not_reviewed",
];

export const DETECTION_GAP_STATUSES: DetectionGapStatus[] = [
  "open",
  "under_review",
  "accepted",
  "resolved",
  "closed",
];

export function toApiDateTime(value: string): string {
  return new Date(value).toISOString();
}

export function optionLabel(id: string | null | undefined, fallback: string): string {
  return id ? `${fallback} (${id.slice(0, 12)})` : fallback;
}
