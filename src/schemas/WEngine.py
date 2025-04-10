from pydantic import BaseModel

from models.Specialty import Specialty
from .Stats import StatsBase

class WEngineBase(BaseModel):
    name: str
    rank: str
    specialty: Specialty
    base_stats: StatsBase
    advanced_stats: StatsBase
    effect: str

class WEngineData(WEngineBase):
    id: int

    class Config:
        from_attributes = True