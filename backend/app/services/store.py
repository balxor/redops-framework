from copy import deepcopy

from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
from app.schemas.common import new_id, utc_now
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.scope import ScopeCreate, ScopeRead, ScopeUpdate


class InMemoryStore:
    def __init__(self) -> None:
        self.projects: dict[str, ProjectRead] = {}
        self.scopes: dict[str, ScopeRead] = {}
        self.assets: dict[str, AssetRead] = {}
        self.campaigns: dict[str, CampaignRead] = {}

    def list_projects(self) -> list[ProjectRead]:
        return list(self.projects.values())

    def create_project(self, payload: ProjectCreate) -> ProjectRead:
        now = utc_now()
        project = ProjectRead(
            **payload.model_dump(),
            project_id=new_id("project"),
            created_at=now,
            updated_at=now,
        )
        self.projects[project.project_id] = project
        return deepcopy(project)

    def get_project(self, project_id: str) -> ProjectRead | None:
        project = self.projects.get(project_id)
        return deepcopy(project) if project else None

    def update_project(self, project_id: str, payload: ProjectUpdate) -> ProjectRead | None:
        project = self.projects.get(project_id)
        if project is None:
            return None
        data = project.model_dump()
        data.update(payload.model_dump(exclude_unset=True))
        data["updated_at"] = utc_now()
        updated = ProjectRead(**data)
        self.projects[project_id] = updated
        return deepcopy(updated)

    def delete_project(self, project_id: str) -> bool:
        if project_id not in self.projects:
            return False
        del self.projects[project_id]
        self.scopes = {key: value for key, value in self.scopes.items() if value.project_id != project_id}
        self.assets = {key: value for key, value in self.assets.items() if value.project_id != project_id}
        self.campaigns = {key: value for key, value in self.campaigns.items() if value.project_id != project_id}
        return True

    def list_scopes(self, project_id: str) -> list[ScopeRead]:
        return [deepcopy(scope) for scope in self.scopes.values() if scope.project_id == project_id]

    def create_scope(self, project_id: str, payload: ScopeCreate) -> ScopeRead:
        now = utc_now()
        scope = ScopeRead(
            **payload.model_dump(),
            scope_id=new_id("scope"),
            project_id=project_id,
            created_at=now,
            updated_at=now,
        )
        self.scopes[scope.scope_id] = scope
        return deepcopy(scope)

    def get_scope(self, project_id: str, scope_id: str) -> ScopeRead | None:
        scope = self.scopes.get(scope_id)
        if scope is None or scope.project_id != project_id:
            return None
        return deepcopy(scope)

    def update_scope(self, project_id: str, scope_id: str, payload: ScopeUpdate) -> ScopeRead | None:
        scope = self.scopes.get(scope_id)
        if scope is None or scope.project_id != project_id:
            return None
        data = scope.model_dump()
        data.update(payload.model_dump(exclude_unset=True))
        data["updated_at"] = utc_now()
        updated = ScopeRead(**data)
        self.scopes[scope_id] = updated
        return deepcopy(updated)

    def list_assets(self, project_id: str) -> list[AssetRead]:
        return [deepcopy(asset) for asset in self.assets.values() if asset.project_id == project_id]

    def create_asset(self, project_id: str, payload: AssetCreate) -> AssetRead:
        now = utc_now()
        asset = AssetRead(
            **payload.model_dump(),
            asset_id=new_id("asset"),
            project_id=project_id,
            created_at=now,
            updated_at=now,
        )
        self.assets[asset.asset_id] = asset
        return deepcopy(asset)

    def get_asset(self, project_id: str, asset_id: str) -> AssetRead | None:
        asset = self.assets.get(asset_id)
        if asset is None or asset.project_id != project_id:
            return None
        return deepcopy(asset)

    def update_asset(self, project_id: str, asset_id: str, payload: AssetUpdate) -> AssetRead | None:
        asset = self.assets.get(asset_id)
        if asset is None or asset.project_id != project_id:
            return None
        data = asset.model_dump()
        data.update(payload.model_dump(exclude_unset=True))
        data["updated_at"] = utc_now()
        updated = AssetRead(**data)
        self.assets[asset_id] = updated
        return deepcopy(updated)

    def delete_asset(self, project_id: str, asset_id: str) -> bool:
        asset = self.assets.get(asset_id)
        if asset is None or asset.project_id != project_id:
            return False
        del self.assets[asset_id]
        return True

    def list_campaigns(self, project_id: str) -> list[CampaignRead]:
        return [deepcopy(campaign) for campaign in self.campaigns.values() if campaign.project_id == project_id]

    def create_campaign(self, project_id: str, payload: CampaignCreate) -> CampaignRead:
        now = utc_now()
        campaign = CampaignRead(
            **payload.model_dump(),
            campaign_id=new_id("campaign"),
            project_id=project_id,
            created_at=now,
            updated_at=now,
        )
        self.campaigns[campaign.campaign_id] = campaign
        return deepcopy(campaign)

    def get_campaign(self, project_id: str, campaign_id: str) -> CampaignRead | None:
        campaign = self.campaigns.get(campaign_id)
        if campaign is None or campaign.project_id != project_id:
            return None
        return deepcopy(campaign)

    def update_campaign(self, project_id: str, campaign_id: str, payload: CampaignUpdate) -> CampaignRead | None:
        campaign = self.campaigns.get(campaign_id)
        if campaign is None or campaign.project_id != project_id:
            return None
        data = campaign.model_dump()
        data.update(payload.model_dump(exclude_unset=True))
        data["updated_at"] = utc_now()
        updated = CampaignRead(**data)
        self.campaigns[campaign_id] = updated
        return deepcopy(updated)


store = InMemoryStore()

