from pydantic import BaseModel

class SkillMultiplierBase(BaseModel):
    name: str
    level: int
    value: str

class SkillMultiplierData(SkillMultiplierBase):
    id: int

    class Config:
        from_attributes = True