from sqlalchemy.orm import Session

from src.models import Bangboo, Faction, Skill, SkillMultiplier, Stats
from src.schemas.Bangboo import BangbooBase

def create_bangboo(db: Session, bangboo: BangbooBase):
    bangboo = Bangboo(
        name=bangboo.name,
        rank=bangboo.rank,
        faction=db.query(Faction).filter(Faction.name == bangboo.faction.name).first() or Faction(**bangboo.faction.model_dump()),
        base_stats=[Stats(**stat.model_dump()) for stat in bangboo.base_stats],
        version_released=bangboo.version_released,
        skills=[Skill(name=skill.name, type=skill.type, description=skill.description, multipliers=[SkillMultiplier(**multiplier.model_dump()) for multiplier in skill.multipliers]) for skill in bangboo.skills]
    )

    db.add(bangboo)
    db.commit()
    db.refresh(bangboo)

    return bangboo


def get_all_bangboo(db: Session):
    return db.query(Bangboo).all()


def get_bangboo(db: Session, bangboo_id: int):
    return db.query(Bangboo).filter(Bangboo.id == bangboo_id).first()


def update_bangboo(db: Session, bangboo_id: int, updated_bangboo: BangbooBase):
    bangboo = get_bangboo(db, bangboo_id)

    if bangboo:
        for key, value in updated_bangboo.model_dump().items():
            if key in ["name", "rank", "version_released"]:
                setattr(bangboo, key, value)
        
        bangboo.faction = db.query(Faction).filter(Faction.name == updated_bangboo.faction.name).first() or Faction(name=updated_bangboo.faction.name)

        db.query(Stats).filter(Stats.bangboo_id == bangboo_id).delete()
        bangboo.base_stats = [Stats(**stats.model_dump()) for stats in updated_bangboo.base_stats]

        for skill in bangboo.skills:
            db.query(SkillMultiplier).filter(SkillMultiplier.skill_id == skill.id).delete()
        db.query(Skill).filter(Skill.bangboo_id == bangboo_id).delete()

        bangboo.skills=[Skill(name=skill.name, type=skill.type, description=skill.description, multipliers=[SkillMultiplier(**multiplier.model_dump()) for multiplier in skill.multipliers]) for skill in updated_bangboo.skills]

        db.commit()
        db.refresh(bangboo)

    return bangboo


def delete_bangboo(db: Session, bangboo_id: int):
    bangboo = get_bangboo(db, bangboo_id)

    if bangboo:
        db.delete(bangboo)
        db.commit()

    return bangboo


def create_or_update_bangboo(db: Session, bangboo: BangbooBase):
    bangboo_in_db = db.query(Bangboo).filter_by(name = bangboo.name).first()

    if bangboo_in_db:
        update_bangboo(db, bangboo_in_db.id, bangboo)
    else:
        create_bangboo(db, bangboo)