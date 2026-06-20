from pydantic import BaseModel, Field


class AttackTechnique(BaseModel):
    technique_id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    tactic_refs: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)
    source: str = "placeholder"

