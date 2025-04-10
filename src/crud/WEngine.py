from sqlalchemy.orm import Session

from models.WEngine import WEngine
from schemas.WEngine import WEngineBase

def create_w_engine(db: Session, w_engine: WEngineBase):
    w_engine = WEngine(**w_engine.model_dump())

    db.add(w_engine)
    db.commit()
    db.refresh(w_engine)

    return w_engine


def get_all_w_engines(db: Session):
    return db.query(WEngine).all()


def get_w_engine(db: Session, w_engine_id: int):
    return db.query(WEngine).filter(WEngine.id == w_engine_id).first()


def update_w_engine(db: Session, w_engine_id: int, update_w_engine: WEngineBase):
    w_engine = get_w_engine(db, w_engine_id)

    if w_engine:
        for key, value in update_w_engine.model_dump().items():
            setattr(w_engine, key, value)

        db.commit()
        db.refresh(w_engine)

    return w_engine


def delete_w_engine(db: Session, w_engine_id: int):
    w_engine = get_w_engine(db, w_engine_id)

    if w_engine:
        db.delete(w_engine)
        db.commit()

    return w_engine