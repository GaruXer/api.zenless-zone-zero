from sqlalchemy.orm import Session

from src.models import Stats
from src.models import WEngine
from src.schemas.WEngine import WEngineBase

def create_w_engine(db: Session, w_engine_data: WEngineBase):
    w_engine = WEngine(
        name=w_engine_data.name,
        rank=w_engine_data.rank,
        specialty=w_engine_data.specialty,
        base_stats = [Stats(**stat.model_dump()) for stat in w_engine_data.base_stats],
        advanced_stats = [Stats(**stat.model_dump()) for stat in w_engine_data.advanced_stats],
        effect=w_engine_data.effect
    )

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
            if key not in ["base_stats", "advanced_stats"]:
                setattr(w_engine, key, value)
            elif key == "base_stats":
                w_engine.base_stats.clear()

                for stats_data in update_w_engine.base_stats:
                    stats = Stats(**stats_data.model_dump())
                    w_engine.base_stats.append(stats)
            elif key == "advanced_stats":
                w_engine.advanced_stats.clear()

                for stats_data in update_w_engine.advanced_stats:
                    stats = Stats(**stats_data.model_dump())
                    w_engine.advanced_stats.append(stats)            

        db.commit()
        db.refresh(w_engine)

    return w_engine


def delete_w_engine(db: Session, w_engine_id: int):
    w_engine = get_w_engine(db, w_engine_id)

    if w_engine:
        db.delete(w_engine)
        db.commit()

    return w_engine


def create_or_update_w_engine(db: Session, w_engine: WEngineBase):
    w_engine_in_db = db.query(WEngine).filter_by(name = w_engine.name).first()

    if w_engine_in_db:
        update_w_engine(db, w_engine_in_db.id, w_engine)
    else:
        create_w_engine(db, w_engine)