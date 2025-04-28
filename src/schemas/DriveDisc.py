from pydantic import BaseModel

class DriveDiscBase(BaseModel):
    name: str
    description_2p_set: str
    description_4p_set: str

class DriveDiscData(DriveDiscBase):
    id: int

    class Config:
        from_attributes = True