from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .Specialty import Specialty
from .Attribute import Attribute

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    specialty = Column(Enum(Specialty, name="specialties"), nullable=False)
    attribute = Column(Enum(Attribute, name="attributes"), nullable=False)
    gender = Column(String)
    height = Column(Integer)
    birthday = Column(String)
    version_released = Column(Float, nullable=False)

    # Foreign Key
    faction_id = Column(Integer, ForeignKey("factions.id"))
    
    # Relations
    faction = relationship("Faction", backref=None, cascade="all")
    voice_actors = relationship("VoiceActor", backref=None, cascade="all, delete-orphan")
    base_stats = relationship("Stats", backref=None, cascade="all, delete-orphan")
    skills = relationship("Skill", backref=None, cascade="all, delete-orphan")
    mindscapes = relationship("Mindscape", backref=None, cascade="all, delete-orphan")