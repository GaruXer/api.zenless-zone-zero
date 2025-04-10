from sqlalchemy.orm import Session

from src.models.DriveDisc import DriveDisc
from src.schemas.DriveDisc import DriveDiscBase

def create_drive_disc(db: Session, drive_disc: DriveDiscBase):
    drive_disc = DriveDisc(**drive_disc.model_dump())

    db.add(drive_disc)
    db.commit()
    db.refresh(drive_disc)

    return drive_disc


def get_all_drive_discs(db: Session):
    return db.query(DriveDisc).all()


def get_drive_disc(db: Session, drive_disc_id: int):
    return db.query(DriveDisc).filter(DriveDisc.id == drive_disc_id).first()


def update_drive_disc(db: Session, drive_disc_id: int, updated_drive_disc: DriveDiscBase):
    drive_disc = get_drive_disc(db, drive_disc_id)

    if drive_disc:
        for key, value in updated_drive_disc.model_dump().items():
            setattr(drive_disc, key, value)

        db.commit()
        db.refresh(drive_disc)

    return drive_disc


def delete_drive_disc(db: Session, drive_disc_id: int):
    drive_disc = get_drive_disc(db, drive_disc_id)

    if drive_disc:
        db.delete(drive_disc)
        db.commit()

    return drive_disc