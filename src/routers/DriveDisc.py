from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import DriveDisc as crud
from database import get_db
from schemas.DriveDisc import DriveDiscBase, DriveDiscData

router = APIRouter(prefix="/drive-disc", tags=["DriveDisc"])

@router.post("/", response_model=DriveDiscData)
def create_drive_disc(drive_disc: DriveDiscBase, db: Session = Depends(get_db)):
    return crud.create_drive_disc(db, drive_disc)


@router.get("/all", response_model=list[DriveDiscData])
def read_all_drive_discs(db: Session = Depends(get_db)):
    return crud.get_all_drive_discs(db)


@router.get("/{drive_disc_id}", response_model=DriveDiscData)
def read_drive_disc(drive_disc_id: int, db: Session = Depends(get_db)):
    drive_disc = crud.get_drive_disc(db, drive_disc_id)

    if not drive_disc:
        raise HTTPException(status_code=404, detail="Drive Disc not found")

    return drive_disc


@router.put("/{drive_disc_id}", response_model=DriveDiscData)
def update_drive_disc(drive_disc_id: int, drive_disc_data: DriveDiscBase, db: Session = Depends(get_db)):
    drive_disc = crud.update_drive_disc(db, drive_disc_id, drive_disc_data)

    if not drive_disc:
        raise HTTPException(status_code=404, detail="Drive Disc not found")

    return drive_disc


@router.delete("/{drive_disc_id}", response_model=DriveDiscData)
def delete_drive_disc(drive_disc_id: int, db: Session = Depends(get_db)):
    drive_disc = crud.delete_drive_disc(db, drive_disc_id)

    if not drive_disc:
        raise HTTPException(status_code=404, detail="Drive Disc not found")

    return drive_disc