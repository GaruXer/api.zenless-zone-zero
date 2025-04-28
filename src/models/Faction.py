from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base

class Faction(Base):
    __tablename__ = "factions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)