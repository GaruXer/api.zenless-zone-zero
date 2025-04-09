from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base

class VoiceActor(Base):
    __tablename__ = "voice_actors"
    
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String)
    actor = Column(String, nullable=False)

    # Foreign Key
    agent_id = Column(Integer, ForeignKey('agents.id'))