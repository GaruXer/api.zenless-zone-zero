from sqlalchemy.orm import Session

from src.models.Bangboo import Bangboo
from src.schemas.Bangboo import BangbooBase

def create_bangboo(db: Session, bangboo: BangbooBase):
    bangboo = Bangboo(**bangboo.model_dump())

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
            setattr(bangboo, key, value)

        db.commit()
        db.refresh(bangboo)

    return bangboo


def delete_bangboo(db: Session, bangboo_id: int):
    bangboo = get_bangboo(db, bangboo_id)

    if bangboo:
        db.delete(bangboo)
        db.commit()

    return bangboo