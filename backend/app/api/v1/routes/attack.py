from fastapi import APIRouter

from app.schemas.attack import AttackTechnique

router = APIRouter()

TECHNIQUES = [
    AttackTechnique(
        technique_id="T1059",
        name="Command and Scripting Interpreter",
        tactic_refs=["execution"],
        platforms=["Windows", "Linux", "macOS", "Cloud"],
        source="placeholder",
    ),
    AttackTechnique(
        technique_id="T1046",
        name="Network Service Discovery",
        tactic_refs=["discovery"],
        platforms=["Windows", "Linux", "macOS"],
        source="placeholder",
    ),
]


@router.get("/techniques", response_model=list[AttackTechnique])
def list_techniques() -> list[AttackTechnique]:
    return TECHNIQUES

