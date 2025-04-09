from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base

class Mindscape(Base):
    __tablename__ = "mindscapes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer)
    description = Column(String)

    # Foreign Key
    agent_id = Column(Integer, ForeignKey('agents.id'))