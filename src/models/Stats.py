from sqlalchemy import Column, Enum, Float, ForeignKey, Integer

from .base import Base
from .StatsType import StatsType

class Stats(Base):
    __tablename__ = "stats"
    
    id = Column(Integer, primary_key=True, index=True)
    stats = Column(Enum(StatsType, name="stats_type"), nullable=False)
    level = Column(Integer)
    value = Column(Float)

    # Foreign Keys
    agent_id = Column(Integer, ForeignKey('agents.id'))
    bangboo_id = Column(Integer, ForeignKey('bangboo.id'))