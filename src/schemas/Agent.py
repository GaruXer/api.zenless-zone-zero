from pydantic import BaseModel

from models.Attribute import Attribute
from models.Specialty import Specialty
from .Faction import FactionBase
from .Mindscape import MindscapeBase
from .Skill import SkillBase
from .Stats import StatsBase
from .VoiceActor import VoiceActorBase

class AgentBase(BaseModel):
    name: str
    full_name: str
    rank: str
    specialty: Specialty
    attribute: Attribute
    gender: str
    faction: FactionBase
    height: int
    birthday: str
    version_released: float
    voice_actors: list[VoiceActorBase]
    base_stats: list[StatsBase]
    skills: list[SkillBase]
    mindscapes: list[MindscapeBase]

class AgentData(AgentBase):
    id: int

    class Config:
        from_attributes = True