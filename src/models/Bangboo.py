from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class Bangboo(Base):
    __tablename__ = "bangboo"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    version_released = Column(Float, nullable=False)

    # Foreign Keys
    faction_id = Column(Integer, ForeignKey('factions.id'))

    # Relations
    faction = relationship("Faction", backref=None, cascade="all")
    base_stats = relationship("Stats", backref=None, cascade="all, delete-orphan")
    skills = relationship("Skill", backref=None, cascade="all, delete-orphan")