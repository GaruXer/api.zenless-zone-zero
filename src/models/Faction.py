from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base

class Faction(Base):
    __tablename__ = "factions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Foreign Keys
    agent_id = Column(Integer, ForeignKey('agents.id'))
    bangboo_id = Column(Integer, ForeignKey('bangboo.id'))