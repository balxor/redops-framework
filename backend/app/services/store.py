from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.campaign import Campaign
from app.models.project import Project
from app.models.scope import Scope
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
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

    def _apply_update(self, model: object, data: dict) -> None:
        if "metadata" in data:
            data["metadata_"] = data.pop("metadata")
        for key, value in data.items():
            setattr(model, key, value)

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


store = DatabaseStore()
