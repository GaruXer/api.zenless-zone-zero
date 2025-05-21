from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import DriveDisc as crud
from src.database import get_db
from src.schemas.DriveDisc import DriveDiscData

router = APIRouter(prefix="/drive-disc", tags=["DriveDisc"])

@router.get("/all", response_model=list[DriveDiscData])
def read_all_drive_discs(db: Session = Depends(get_db)):
    return crud.get_all_drive_discs(db)


@router.get("/{drive_disc_id}", response_model=DriveDiscData)
def read_drive_disc(drive_disc_id: int, db: Session = Depends(get_db)):
    drive_disc = crud.get_drive_disc(db, drive_disc_id)

    if not drive_disc:
        raise HTTPException(status_code=404, detail="Drive Disc not found")

    return drive_disc