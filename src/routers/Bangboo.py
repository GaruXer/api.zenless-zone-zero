from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import Bangboo as crud
from database import get_db
from schemas.Bangboo import BangbooBase, BangbooData

router = APIRouter(prefix="/bangboo", tags=["Bangboo"])

@router.post("/", response_model=BangbooData)
def create_bangboo(bangboo: BangbooBase, db: Session = Depends(get_db)):
    return crud.create_bangboo(db, bangboo)


@router.get("/all", response_model=list[BangbooData])
def read_all_bangboo(db: Session = Depends(get_db)):
    return crud.get_all_bangboo(db)


@router.get("/{bangboo_id}", response_model=BangbooData)
def read_bangboo(bangboo_id: int, db: Session = Depends(get_db)):
    bangboo = crud.get_bangboo(db, bangboo_id)

    if not bangboo:
        raise HTTPException(status_code=404, detail="Bangboo not found")

    return bangboo


@router.put("/{bangboo_id}", response_model=BangbooData)
def update_bangboo(bangboo_id: int, bangboo_data: BangbooBase, db: Session = Depends(get_db)):
    bangboo = crud.update_bangboo(db, bangboo_id, bangboo_data)

    if not bangboo:
        raise HTTPException(status_code=404, detail="Bangboo not found")

    return bangboo


@router.delete("/{bangboo_id}", response_model=BangbooData)
def delete_bangboo(bangboo_id: int, db: Session = Depends(get_db)):
    bangboo = crud.delete_bangboo(db, bangboo_id)

    if not bangboo:
        raise HTTPException(status_code=404, detail="Bangboo not found")

    return bangboo