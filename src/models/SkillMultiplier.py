from sqlalchemy import Column, Float, ForeignKey, Integer, String

from .base import Base

class SkillMultiplier(Base):
    __tablename__ = "skills_multipliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer)
    value = Column(Float)

    # Foreign Key
    skill_id = Column(Integer, ForeignKey("skills.id"))