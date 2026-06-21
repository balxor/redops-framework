from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.campaign import Campaign
from app.models.action import Action
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.report import Report
from app.models.project import Project
from app.models.scope import Scope
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
from app.schemas.action import ActionCreate, ActionRead, ActionUpdate
from app.schemas.evidence import EvidenceCreate, EvidenceRead, EvidenceUpdate
from app.schemas.finding import FindingCreate, FindingRead, FindingUpdate
from app.schemas.report import ReportCreate, ReportRead, ReportUpdate
from app.schemas.common import new_id, utc_now
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.scope import ScopeCreate, ScopeRead, ScopeUpdate


class DatabaseStore:
    def list_projects(self, db: Session, project_ids: list[str] | None = None) -> list[ProjectRead]:
        statement = select(Project)
        if project_ids is not None:
            if not project_ids:
                return []
            statement = statement.where(Project.project_id.in_(project_ids))
        return [self._project_read(project) for project in db.scalars(statement).all()]

    def create_project(self, db: Session, payload: ProjectCreate) -> ProjectRead:
        now = utc_now()
        project = Project(
            **payload.model_dump(exclude={"metadata"}),
            project_id=new_id("project"),
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return self._project_read(project)

    def get_project(self, db: Session, project_id: str) -> ProjectRead | None:
        project = db.get(Project, project_id)
        return self._project_read(project) if project else None

    def update_project(self, db: Session, project_id: str, payload: ProjectUpdate) -> ProjectRead | None:
        project = db.get(Project, project_id)
        if project is None:
            return None
        self._apply_update(project, payload.model_dump(exclude_unset=True))
        project.updated_at = utc_now()
        db.commit()
        db.refresh(project)
        return self._project_read(project)

    def delete_project(self, db: Session, project_id: str) -> bool:
        project = db.get(Project, project_id)
        if project is None:
            return False
        db.delete(project)
        db.commit()
        return True

    def list_scopes(self, db: Session, project_id: str) -> list[ScopeRead]:
        statement = select(Scope).where(Scope.project_id == project_id)
        return [self._scope_read(scope) for scope in db.scalars(statement).all()]

    def create_scope(self, db: Session, project_id: str, payload: ScopeCreate) -> ScopeRead:
        now = utc_now()
        scope = Scope(
            **payload.model_dump(mode="json", exclude={"metadata"}),
            scope_id=new_id("scope"),
            project_id=project_id,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(scope)
        db.commit()
        db.refresh(scope)
        return self._scope_read(scope)

    def get_scope(self, db: Session, project_id: str, scope_id: str) -> ScopeRead | None:
        scope = db.get(Scope, scope_id)
        if scope is None or scope.project_id != project_id:
            return None
        return self._scope_read(scope)

    def update_scope(self, db: Session, project_id: str, scope_id: str, payload: ScopeUpdate) -> ScopeRead | None:
        scope = db.get(Scope, scope_id)
        if scope is None or scope.project_id != project_id:
            return None
        self._apply_update(scope, payload.model_dump(mode="json", exclude_unset=True))
        scope.updated_at = utc_now()
        db.commit()
        db.refresh(scope)
        return self._scope_read(scope)

    def list_assets(self, db: Session, project_id: str) -> list[AssetRead]:
        statement = select(Asset).where(Asset.project_id == project_id)
        return [self._asset_read(asset) for asset in db.scalars(statement).all()]

    def create_asset(self, db: Session, project_id: str, payload: AssetCreate) -> AssetRead:
        now = utc_now()
        asset = Asset(
            **payload.model_dump(exclude={"metadata"}),
            asset_id=new_id("asset"),
            project_id=project_id,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return self._asset_read(asset)

    def get_asset(self, db: Session, project_id: str, asset_id: str) -> AssetRead | None:
        asset = db.get(Asset, asset_id)
        if asset is None or asset.project_id != project_id:
            return None
        return self._asset_read(asset)

    def update_asset(self, db: Session, project_id: str, asset_id: str, payload: AssetUpdate) -> AssetRead | None:
        asset = db.get(Asset, asset_id)
        if asset is None or asset.project_id != project_id:
            return None
        self._apply_update(asset, payload.model_dump(exclude_unset=True))
        asset.updated_at = utc_now()
        db.commit()
        db.refresh(asset)
        return self._asset_read(asset)

    def delete_asset(self, db: Session, project_id: str, asset_id: str) -> bool:
        asset = db.get(Asset, asset_id)
        if asset is None or asset.project_id != project_id:
            return False
        db.delete(asset)
        db.commit()
        return True

    def list_campaigns(self, db: Session, project_id: str) -> list[CampaignRead]:
        statement = select(Campaign).where(Campaign.project_id == project_id)
        return [self._campaign_read(campaign) for campaign in db.scalars(statement).all()]

    def create_campaign(self, db: Session, project_id: str, payload: CampaignCreate) -> CampaignRead:
        now = utc_now()
        campaign = Campaign(
            **payload.model_dump(mode="json", exclude={"metadata"}),
            campaign_id=new_id("campaign"),
            project_id=project_id,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return self._campaign_read(campaign)

    def get_campaign(self, db: Session, project_id: str, campaign_id: str) -> CampaignRead | None:
        campaign = db.get(Campaign, campaign_id)
        if campaign is None or campaign.project_id != project_id:
            return None
        return self._campaign_read(campaign)

    def update_campaign(
        self,
        db: Session,
        project_id: str,
        campaign_id: str,
        payload: CampaignUpdate,
    ) -> CampaignRead | None:
        campaign = db.get(Campaign, campaign_id)
        if campaign is None or campaign.project_id != project_id:
            return None
        self._apply_update(campaign, payload.model_dump(mode="json", exclude_unset=True))
        campaign.updated_at = utc_now()
        db.commit()
        db.refresh(campaign)
        return self._campaign_read(campaign)

    def list_actions(self, db: Session, project_id: str) -> list[ActionRead]:
        statement = select(Action).where(Action.project_id == project_id).order_by(Action.created_at)
        return [self._action_read(action) for action in db.scalars(statement).all()]

    def create_action(
        self,
        db: Session,
        project_id: str,
        operator_id: str,
        payload: ActionCreate,
    ) -> ActionRead:
        self._validate_action_references(db, project_id, payload.model_dump(mode="json"))
        now = utc_now()
        action = Action(
            **payload.model_dump(exclude={"metadata"}),
            action_id=new_id("action"),
            project_id=project_id,
            operator_id=operator_id,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(action)
        db.commit()
        db.refresh(action)
        return self._action_read(action)

    def get_action(self, db: Session, project_id: str, action_id: str) -> ActionRead | None:
        action = db.get(Action, action_id)
        if action is None or action.project_id != project_id:
            return None
        return self._action_read(action)

    def update_action(
        self,
        db: Session,
        project_id: str,
        action_id: str,
        payload: ActionUpdate,
    ) -> ActionRead | None:
        action = db.get(Action, action_id)
        if action is None or action.project_id != project_id:
            return None
        self._validate_action_references(db, project_id, payload.model_dump(mode="json", exclude_unset=True))
        self._apply_update(action, payload.model_dump(exclude_unset=True))
        action.updated_at = utc_now()
        db.commit()
        db.refresh(action)
        return self._action_read(action)

    def list_evidence(self, db: Session, project_id: str) -> list[EvidenceRead]:
        statement = select(Evidence).where(Evidence.project_id == project_id).order_by(Evidence.created_at)
        return [self._evidence_read(evidence) for evidence in db.scalars(statement).all()]

    def create_evidence(
        self,
        db: Session,
        project_id: str,
        uploaded_by: str,
        payload: EvidenceCreate,
    ) -> EvidenceRead:
        self._validate_evidence_references(db, project_id, payload.model_dump(mode="json"))
        now = utc_now()
        evidence = Evidence(
            **payload.model_dump(exclude={"metadata"}),
            evidence_id=new_id("evidence"),
            project_id=project_id,
            uploaded_by=uploaded_by,
            uploaded_at=now,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        return self._evidence_read(evidence)

    def get_evidence(self, db: Session, project_id: str, evidence_id: str) -> EvidenceRead | None:
        evidence = db.get(Evidence, evidence_id)
        if evidence is None or evidence.project_id != project_id:
            return None
        return self._evidence_read(evidence)

    def update_evidence(
        self,
        db: Session,
        project_id: str,
        evidence_id: str,
        payload: EvidenceUpdate,
    ) -> EvidenceRead | None:
        evidence = db.get(Evidence, evidence_id)
        if evidence is None or evidence.project_id != project_id:
            return None
        self._validate_evidence_references(db, project_id, payload.model_dump(mode="json", exclude_unset=True))
        self._apply_update(evidence, payload.model_dump(exclude_unset=True))
        evidence.updated_at = utc_now()
        db.commit()
        db.refresh(evidence)
        return self._evidence_read(evidence)

    def list_findings(self, db: Session, project_id: str) -> list[FindingRead]:
        statement = select(Finding).where(Finding.project_id == project_id).order_by(Finding.created_at)
        return [self._finding_read(finding) for finding in db.scalars(statement).all()]

    def create_finding(
        self,
        db: Session,
        project_id: str,
        created_by: str,
        payload: FindingCreate,
    ) -> FindingRead:
        self._validate_finding_references(db, project_id, payload.model_dump(mode="json"))
        now = utc_now()
        finding = Finding(
            **payload.model_dump(mode="json", exclude={"metadata"}),
            finding_id=new_id("finding"),
            project_id=project_id,
            created_by=created_by,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(finding)
        db.commit()
        db.refresh(finding)
        return self._finding_read(finding)

    def get_finding(self, db: Session, project_id: str, finding_id: str) -> FindingRead | None:
        finding = db.get(Finding, finding_id)
        if finding is None or finding.project_id != project_id:
            return None
        return self._finding_read(finding)

    def update_finding(
        self,
        db: Session,
        project_id: str,
        finding_id: str,
        payload: FindingUpdate,
    ) -> FindingRead | None:
        finding = db.get(Finding, finding_id)
        if finding is None or finding.project_id != project_id:
            return None
        self._validate_finding_references(db, project_id, payload.model_dump(mode="json", exclude_unset=True))
        self._apply_update(finding, payload.model_dump(mode="json", exclude_unset=True))
        finding.updated_at = utc_now()
        db.commit()
        db.refresh(finding)
        return self._finding_read(finding)

    def list_reports(self, db: Session, project_id: str) -> list[ReportRead]:
        statement = select(Report).where(Report.project_id == project_id).order_by(Report.created_at)
        return [self._report_read(report) for report in db.scalars(statement).all()]

    def create_report(
        self,
        db: Session,
        project_id: str,
        payload: ReportCreate,
    ) -> ReportRead:
        self._validate_report_references(db, project_id, payload.model_dump(mode="json"))
        now = utc_now()
        report = Report(
            **payload.model_dump(exclude={"metadata"}),
            report_id=new_id("report"),
            project_id=project_id,
            metadata_=payload.metadata,
            created_at=now,
            updated_at=now,
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return self._report_read(report)

    def get_report(self, db: Session, project_id: str, report_id: str) -> ReportRead | None:
        report = db.get(Report, report_id)
        if report is None or report.project_id != project_id:
            return None
        return self._report_read(report)

    def update_report(
        self,
        db: Session,
        project_id: str,
        report_id: str,
        payload: ReportUpdate,
    ) -> ReportRead | None:
        report = db.get(Report, report_id)
        if report is None or report.project_id != project_id:
            return None
        self._validate_report_references(db, project_id, payload.model_dump(mode="json", exclude_unset=True))
        self._apply_update(report, payload.model_dump(exclude_unset=True))
        report.updated_at = utc_now()
        db.commit()
        db.refresh(report)
        return self._report_read(report)

    def _apply_update(self, model: object, data: dict) -> None:
        if "metadata" in data:
            data["metadata_"] = data.pop("metadata")
        for key, value in data.items():
            setattr(model, key, value)

    def _validate_action_references(self, db: Session, project_id: str, data: dict) -> None:
        self._ensure_project_ref(db, Campaign, data.get("campaign_id"), project_id, "Campaign")
        self._ensure_project_ref(db, Asset, data.get("asset_id"), project_id, "Asset")

    def _validate_evidence_references(self, db: Session, project_id: str, data: dict) -> None:
        self._ensure_project_ref(db, Action, data.get("action_id"), project_id, "Action")
        self._ensure_project_ref(db, Asset, data.get("asset_id"), project_id, "Asset")
        self._ensure_project_ref(db, Finding, data.get("finding_id"), project_id, "Finding")

    def _validate_finding_references(self, db: Session, project_id: str, data: dict) -> None:
        self._ensure_project_refs(db, Asset, data.get("affected_assets"), project_id, "Asset")
        self._ensure_project_refs(db, Evidence, data.get("evidence_ids"), project_id, "Evidence")

    def _validate_report_references(self, db: Session, project_id: str, data: dict) -> None:
        self._ensure_project_refs(db, Finding, data.get("finding_ids"), project_id, "Finding")
        self._ensure_project_refs(db, Evidence, data.get("evidence_ids"), project_id, "Evidence")

    def _ensure_project_refs(
        self,
        db: Session,
        model: type,
        ids: list[str] | None,
        project_id: str,
        label: str,
    ) -> None:
        if ids is None:
            return
        for entity_id in ids:
            self._ensure_project_ref(db, model, entity_id, project_id, label)

    def _ensure_project_ref(
        self,
        db: Session,
        model: type,
        entity_id: str | None,
        project_id: str,
        label: str,
    ) -> None:
        if entity_id is None:
            return
        entity = db.get(model, entity_id)
        if entity is None or getattr(entity, "project_id", None) != project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{label} reference is invalid for this project",
            )

    def _project_read(self, project: Project) -> ProjectRead:
        return ProjectRead(
            project_id=project.project_id,
            name=project.name,
            engagement_type=project.engagement_type,
            status=project.status,
            client_name=project.client_name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            timezone=project.timezone,
            tags=project.tags,
            metadata=project.metadata_,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    def _scope_read(self, scope: Scope) -> ScopeRead:
        return ScopeRead(
            scope_id=scope.scope_id,
            project_id=scope.project_id,
            status=scope.status,
            allowed_targets=scope.allowed_targets,
            forbidden_targets=scope.forbidden_targets,
            test_window=scope.test_window,
            rules_of_engagement=scope.rules_of_engagement,
            restricted_actions=scope.restricted_actions,
            approval_required=scope.approval_required,
            notes=scope.notes,
            metadata=scope.metadata_,
            created_at=scope.created_at,
            updated_at=scope.updated_at,
        )

    def _asset_read(self, asset: Asset) -> AssetRead:
        return AssetRead(
            asset_id=asset.asset_id,
            project_id=asset.project_id,
            scope_id=asset.scope_id,
            value=asset.value,
            type=asset.type,
            environment=asset.environment,
            criticality=asset.criticality,
            tags=asset.tags,
            metadata=asset.metadata_,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
        )

    def _campaign_read(self, campaign: Campaign) -> CampaignRead:
        return CampaignRead(
            campaign_id=campaign.campaign_id,
            project_id=campaign.project_id,
            name=campaign.name,
            objective=campaign.objective,
            status=campaign.status,
            steps=campaign.steps,
            tags=campaign.tags,
            metadata=campaign.metadata_,
            created_at=campaign.created_at,
            updated_at=campaign.updated_at,
        )

    def _action_read(self, action: Action) -> ActionRead:
        return ActionRead(
            action_id=action.action_id,
            project_id=action.project_id,
            campaign_id=action.campaign_id,
            campaign_step_id=action.campaign_step_id,
            asset_id=action.asset_id,
            operator_id=action.operator_id,
            action_type=action.action_type,
            action_summary=action.action_summary,
            action_detail=action.action_detail,
            result=action.result,
            detection_status=action.detection_status,
            started_at=action.started_at,
            ended_at=action.ended_at,
            metadata=action.metadata_,
            created_at=action.created_at,
            updated_at=action.updated_at,
        )

    def _evidence_read(self, evidence: Evidence) -> EvidenceRead:
        return EvidenceRead(
            evidence_id=evidence.evidence_id,
            project_id=evidence.project_id,
            action_id=evidence.action_id,
            finding_id=evidence.finding_id,
            asset_id=evidence.asset_id,
            uploaded_by=evidence.uploaded_by,
            evidence_type=evidence.evidence_type,
            file_name=evidence.file_name,
            file_size=evidence.file_size,
            mime_type=evidence.mime_type,
            file_hash_sha256=evidence.file_hash_sha256,
            description=evidence.description,
            sanitized=evidence.sanitized,
            captured_at=evidence.captured_at,
            uploaded_at=evidence.uploaded_at,
            metadata=evidence.metadata_,
            created_at=evidence.created_at,
            updated_at=evidence.updated_at,
        )

    def _finding_read(self, finding: Finding) -> FindingRead:
        return FindingRead(
            finding_id=finding.finding_id,
            project_id=finding.project_id,
            title=finding.title,
            summary=finding.summary,
            severity=finding.severity,
            status=finding.status,
            affected_assets=finding.affected_assets,
            attack_technique_id=finding.attack_technique_id,
            attack_mapping=finding.attack_mapping,
            evidence_ids=finding.evidence_ids,
            impact=finding.impact,
            likelihood=finding.likelihood or "unknown",
            recommendation=finding.recommendation,
            reviewed_by=finding.reviewed_by,
            metadata=finding.metadata_,
            created_by=finding.created_by,
            created_at=finding.created_at,
            updated_at=finding.updated_at,
        )

    def _report_read(self, report: Report) -> ReportRead:
        return ReportRead(
            report_id=report.report_id,
            project_id=report.project_id,
            title=report.title,
            version=report.version,
            status=report.status,
            format=report.format,
            file_path=report.file_path,
            finding_ids=report.finding_ids,
            evidence_ids=report.evidence_ids,
            sections=report.sections,
            prepared_by=report.prepared_by,
            reviewed_by=report.reviewed_by,
            generated_by=report.generated_by,
            generated_at=report.generated_at,
            published_at=report.published_at,
            metadata=report.metadata_,
            created_at=report.created_at,
            updated_at=report.updated_at,
        )


store = DatabaseStore()
