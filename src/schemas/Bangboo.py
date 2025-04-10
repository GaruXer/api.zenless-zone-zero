from pydantic import BaseModel

from .Faction import FactionBase
from .Skill import SkillBase
from .Stats import StatsBase

class BangbooBase(BaseModel):
    name: str
    rank: str
    faction: FactionBase
    base_stats: list[StatsBase]
    version_released: float
    skills: list[SkillBase]

class BangbooData(BangbooBase):
    id: int

    class Config:
        from_attributes = True