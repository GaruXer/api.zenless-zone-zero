from sqlalchemy import Column, Integer, String

from .base import Base

class DriveDisc(Base):
    __tablename__ = "drive_discs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rarity = Column(String, nullable=False)
    description_2p_set = Column(String)
    description_4p_set = Column(String)