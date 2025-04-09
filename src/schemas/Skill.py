from pydantic import BaseModel

from models.SkillType import SkillType
from .SkillMultiplier import SkillMultiplierBase

class SkillBase(BaseModel):
    name: str
    type: SkillType
    description: str
    multipliers: list[SkillMultiplierBase]

class SkillData(SkillBase):
    id: int

    class Config:
        orm_mode = True