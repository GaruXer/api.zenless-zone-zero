from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import Bangboo as crud
from src.database import get_db
from src.schemas.Bangboo import BangbooData

router = APIRouter(prefix="/bangboo", tags=["Bangboo"])

@router.get("/all", response_model=list[BangbooData])
def read_all_bangboo(db: Session = Depends(get_db)):
    return crud.get_all_bangboo(db)


@router.get("/{bangboo_id}", response_model=BangbooData)
def read_bangboo(bangboo_id: int, db: Session = Depends(get_db)):
    bangboo = crud.get_bangboo(db, bangboo_id)

    if not bangboo:
        raise HTTPException(status_code=404, detail="Bangboo not found")

    return bangboo