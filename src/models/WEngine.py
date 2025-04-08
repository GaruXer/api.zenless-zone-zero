from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .Specialty import Specialty

class WEngine(Base):
    __tablename__ = "w_engines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    specialty = Column(Enum(Specialty, name="specialty"), nullable=False)
    effect = Column(String)

    # Foreign Keys
    base_stats_id = Column(Integer, ForeignKey('stats.id'))
    advanced_stats_id = Column(Integer, ForeignKey('stats.id'))

    # Relations
    base_stats = relationship("Stats", foreign_keys=[base_stats_id], uselist=False)
    advanced_stats = relationship("Stats", foreign_keys=[advanced_stats_id], uselist=False)