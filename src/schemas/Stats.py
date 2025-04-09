from pydantic import BaseModel

from models.StatsType import StatsType

class StatsBase(BaseModel):
    stats: StatsType
    level: int
    value: float

class StatsData(StatsBase):
    id: int

    class Config:
        orm_mode = True