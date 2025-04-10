from pydantic import BaseModel

class MindscapeBase(BaseModel):
    name: str
    level: int
    description: str

class MindscapeData(MindscapeBase):
    id: int

    class Config:
        from_attributes = True