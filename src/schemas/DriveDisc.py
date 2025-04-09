from pydantic import BaseModel

class DriveDiscBase(BaseModel):
    name: str
    rarity: str
    description_2p_set: str
    description_4p_set: str

class DriveDiscData(DriveDiscBase):
    id: int

    class Config:
        orm_mode = True