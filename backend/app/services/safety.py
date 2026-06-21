from ipaddress import ip_address, ip_network

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scope import Scope
from app.services.approvals import has_active_approval
from app.schemas.action import ActionCreate, ActionUpdate
from app.schemas.asset import AssetCreate, AssetUpdate
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.schemas.safety import SafetySummary


def get_safety_summary(db: Session, project_id: str) -> SafetySummary:
    scopes = _approved_scopes(db, project_id)
    restricted_actions = sorted(
        {
            action
            for scope in scopes
            for action in (scope.restricted_actions or [])
        }
    )
    return SafetySummary(
        project_id=project_id,
        approved_scope_count=len(scopes),
        has_approved_scope=bool(scopes),
        restricted_actions=restricted_actions,
    )


def validate_asset_create(db: Session, project_id: str, payload: AssetCreate) -> None:
    scopes = _require_approved_scope(db, project_id)
    _validate_asset_value(scopes, payload.value, payload.type)


def validate_asset_update(db: Session, project_id: str, payload: AssetUpdate) -> None:
    if payload.value is None and payload.type is None:
        return
    scopes = _require_approved_scope(db, project_id)
    if payload.value is None or payload.type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset value and type are required when updating scope-bound asset target data",
        )
    _validate_asset_value(scopes, payload.value, payload.type)


def validate_campaign_create(db: Session, project_id: str, payload: CampaignCreate) -> None:
    _require_approved_scope(db, project_id)
    _validate_campaign_steps(payload.steps)


def validate_campaign_update(db: Session, project_id: str, campaign_id: str, payload: CampaignUpdate) -> None:
    _require_approved_scope(db, project_id)
    if payload.steps is not None:
        _validate_campaign_steps(payload.steps)
    if _campaign_update_requires_approval(payload) and not has_active_approval(db, project_id, "campaign", campaign_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Approved campaign approval is required before approving or activating campaign workflow",
        )


def validate_action_create(db: Session, project_id: str, payload: ActionCreate) -> None:
    _require_approved_scope(db, project_id)
    _validate_restricted_action_approval(db, project_id, payload.action_type)


def validate_action_update(db: Session, project_id: str, payload: ActionUpdate) -> None:
    _require_approved_scope(db, project_id)
    if payload.action_type is not None:
        _validate_restricted_action_approval(db, project_id, payload.action_type)


def _approved_scopes(db: Session, project_id: str) -> list[Scope]:
    statement = select(Scope).where(Scope.project_id == project_id, Scope.status == "approved")
    return list(db.scalars(statement).all())


def _require_approved_scope(db: Session, project_id: str) -> list[Scope]:
    scopes = _approved_scopes(db, project_id)
    if not scopes:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Approved project scope is required before creating scope-bound resources",
        )
    return scopes


def _validate_asset_value(scopes: list[Scope], value: str, asset_type: str) -> None:
    if any(_target_matches(target, value, asset_type) for scope in scopes for target in scope.forbidden_targets):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Asset target is explicitly forbidden by scope")

    if not any(_target_matches(target, value, asset_type) for scope in scopes for target in scope.allowed_targets):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Asset target is outside approved scope")


def _target_matches(target: dict, value: str, asset_type: str) -> bool:
    target_type = target.get("type")
    target_value = str(target.get("value", "")).lower()
    normalized_value = value.lower()

    if target_type == "ip_range":
        try:
            return ip_address(value) in ip_network(target_value, strict=False)
        except ValueError:
            return False

    if target_type == "ip_address":
        return asset_type == "ip_address" and normalized_value == target_value

    if target_type in {"domain", "subdomain"}:
        return asset_type in {"domain", "host"} and normalized_value == target_value

    if target_type in {"url", "application", "api"}:
        return normalized_value == target_value

    return normalized_value == target_value


def _validate_campaign_steps(steps: list) -> None:
    for step in steps:
        if step.status in {"approved", "executed"} and not step.approval_required:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Approved or executed campaign steps must keep approval_required enabled",
            )


def _campaign_update_requires_approval(payload: CampaignUpdate) -> bool:
    if payload.status in {"approved", "active"}:
        return True
    if payload.steps is None:
        return False
    return any(step.status in {"approved", "executed"} for step in payload.steps)


def _validate_restricted_action_approval(db: Session, project_id: str, action_type: str) -> None:
    restricted = _restricted_action_categories(db, project_id)
    category = _restricted_category_for_action_type(action_type)
    if category is None or category not in restricted:
        return
    if has_active_approval(db, project_id, "action_type", action_type):
        return
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Approved action_type approval is required for restricted action {action_type}",
    )


def _restricted_action_categories(db: Session, project_id: str) -> set[str]:
    return {
        action
        for scope in _approved_scopes(db, project_id)
        for action in (scope.restricted_actions or [])
    }


def _restricted_category_for_action_type(action_type: str) -> str | None:
    mapping = {
        "exploit_validation_note": "exploit_validation",
        "scanner_result": "external_tool_execution",
    }
    return mapping.get(action_type)
