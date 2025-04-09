from pydantic import BaseModel

class FactionBase(BaseModel):
    name: str

class FactionData(FactionBase):
    id: int

    class Config:
        orm_mode = True