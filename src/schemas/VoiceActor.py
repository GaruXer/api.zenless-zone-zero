from pydantic import BaseModel

class VoiceActorBase(BaseModel):
    language: str
    actor: str

class VoiceActorData(VoiceActorBase):
    id: int

    class Config:
        from_attributes = True