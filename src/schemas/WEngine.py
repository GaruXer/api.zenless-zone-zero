from pydantic import BaseModel

from src.models.Specialty import Specialty
from .Stats import StatsBase

class WEngineBase(BaseModel):
    name: str
    rank: str
    specialty: Specialty
    base_stats: list[StatsBase]
    advanced_stats: list[StatsBase]
    effect: str

class WEngineData(WEngineBase):
    id: int

    class Config:
        from_attributes = True