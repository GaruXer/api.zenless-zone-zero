from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .SkillType import SkillType

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(SkillType, name="skill_type"), nullable=False)
    description = Column(String)

    # Foreign Keys
    agent_id = Column(Integer, ForeignKey('agents.id'))
    bangboo_id = Column(Integer, ForeignKey('bangboo.id'))

    # Relation
    multipliers = relationship("SkillMultiplier", backref=None, cascade="all, delete-orphan")