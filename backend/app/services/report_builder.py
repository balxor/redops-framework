from sqlalchemy.orm import Session

from app.schemas.common import utc_now
from app.schemas.report import ReportCreate, ReportGenerateRequest, ReportSection
from app.services.store import store

DEFAULT_SECTIONS = [
    "executive_summary",
    "scope",
    "campaign_summary",
    "action_summary",
    "findings_summary",
    "evidence_appendix",
    "limitations",
]


def build_report_outline(db: Session, project_id: str, generated_by: str, payload: ReportGenerateRequest) -> ReportCreate:
    project = store.get_project(db, project_id)
    scopes = store.list_scopes(db, project_id)
    assets = store.list_assets(db, project_id)
    campaigns = store.list_campaigns(db, project_id)
    actions = store.list_actions(db, project_id)
    evidence = store.list_evidence(db, project_id)
    findings = store.list_findings(db, project_id)

    included = payload.include_sections or DEFAULT_SECTIONS
    section_builders = {
        "executive_summary": lambda: _section(
            "executive_summary",
            "Executive Summary",
            [
                f"Project: {project.name if project else project_id}",
                f"Engagement type: {project.engagement_type if project else 'unknown'}",
                f"Current status: {project.status if project else 'unknown'}",
                f"Findings recorded: {len(findings)}",
                f"Actions recorded: {len(actions)}",
            ],
            1,
        ),
        "scope": lambda: _section(
            "scope",
            "Scope",
            [
                f"Approved scopes: {sum(1 for scope in scopes if scope.status == 'approved')}",
                f"Allowed targets: {sum(len(scope.allowed_targets) for scope in scopes)}",
                f"Forbidden targets: {sum(len(scope.forbidden_targets) for scope in scopes)}",
                f"Registered assets: {len(assets)}",
            ],
            2,
        ),
        "campaign_summary": lambda: _section(
            "campaign_summary",
            "Campaign Summary",
            [f"- {campaign.name}: {campaign.status} ({len(campaign.steps)} steps)" for campaign in campaigns] or ["No campaigns recorded."],
            3,
        ),
        "action_summary": lambda: _section(
            "action_summary",
            "Action Summary",
            [f"- {action.action_summary}: {action.result}, detection {action.detection_status}" for action in actions] or ["No actions recorded."],
            4,
        ),
        "findings_summary": lambda: _section(
            "findings_summary",
            "Findings Summary",
            [f"- {finding.title}: {finding.severity}, {finding.status}" for finding in findings] or ["No findings recorded."],
            5,
        ),
        "evidence_appendix": lambda: _section(
            "evidence_appendix",
            "Evidence Appendix",
            [f"- {item.evidence_type}: {item.description}" for item in evidence] or ["No evidence recorded."],
            6,
        ),
        "limitations": lambda: _section(
            "limitations",
            "Limitations",
            [
                "This outline is generated from recorded project metadata only.",
                "Human review is required before publication.",
                "Sensitive details and client-specific data should be reviewed before export.",
            ],
            7,
        ),
    }

    sections = [section_builders[key]() for key in included if key in section_builders]
    return ReportCreate(
        title=payload.title,
        version="0.1",
        status="generated",
        format=payload.format,
        finding_ids=[finding.finding_id for finding in findings],
        evidence_ids=[item.evidence_id for item in evidence],
        sections=sections,
        generated_by=generated_by,
        generated_at=utc_now(),
        metadata={"generated_from": "project_outline"},
    )


def _section(key: str, title: str, lines: list[str], order: int) -> ReportSection:
    return ReportSection(key=key, title=title, content="\n".join(lines), order=order)
