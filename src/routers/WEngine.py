from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import WEngine as crud
from src.database import get_db
from src.schemas.WEngine import WEngineData

router = APIRouter(prefix="/w-engine", tags=["WEngine"])

@router.get("/all", response_model=list[WEngineData])
def read_all_w_engines(db: Session = Depends(get_db)):
    return crud.get_all_w_engines(db)


@router.get("/{w_engine_id}", response_model=WEngineData)
def read_w_engine(w_engine_id: int, db: Session = Depends(get_db)):
    w_engine = crud.get_w_engine(db, w_engine_id)

    if not w_engine:
        raise HTTPException(status_code=404, detail="W-Engine not found")

    return w_engine