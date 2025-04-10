from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import WEngine as crud
from database import get_db
from schemas.WEngine import WEngineBase, WEngineData

router = APIRouter(prefix="/w-engine", tags=["WEngine"])

@router.post("/", response_model=WEngineData)
def create_w_engine(w_engine: WEngineBase, db: Session = Depends(get_db)):
    return crud.create_w_engine(db, w_engine)


@router.get("/all", response_model=list[WEngineData])
def read_all_w_engines(db: Session = Depends(get_db)):
    return crud.get_all_w_engines(db)


@router.get("/{w_engine_id}", response_model=WEngineData)
def read_w_engine(w_engine_id: int, db: Session = Depends(get_db)):
    w_engine = crud.get_w_engine(db, w_engine_id)

    if not w_engine:
        raise HTTPException(status_code=404, detail="W-Engine not found")

    return w_engine


@router.put("/{w_engine_id}", response_model=WEngineData)
def update_w_engine(w_engine_id: int, w_engine_data: WEngineBase, db: Session = Depends(get_db)):
    w_engine = crud.update_w_engine(db, w_engine_id, w_engine_data)

    if not w_engine:
        raise HTTPException(status_code=404, detail="W-Engine not found")

    return w_engine


@router.delete("/{w_engine_id}", response_model=WEngineData)
def delete_w_engine(w_engine_id: int, db: Session = Depends(get_db)):
    w_engine = crud.delete_w_engine(db, w_engine_id)

    if not w_engine:
        raise HTTPException(status_code=404, detail="W-Engine not found")

    return w_engine