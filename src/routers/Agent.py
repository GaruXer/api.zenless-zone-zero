from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import Agent as crud
from src.database import get_db
from src.schemas.Agent import AgentBase, AgentData

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/", response_model=AgentData)
def create_agent(agent: AgentBase, db: Session = Depends(get_db)):
    return crud.create_agent(db, agent)


@router.get("/all", response_model=list[AgentData])
def read_all_agents(db: Session = Depends(get_db)):
    return crud.get_all_agents(db)


@router.get("/{agent_id}", response_model=AgentData)
def read_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = crud.get_agent(db, agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


@router.put("/{agent_id}", response_model=AgentData)
def update_agent(agent_id: int, agent_data: AgentBase, db: Session = Depends(get_db)):
    agent = crud.update_agent(db, agent_id, agent_data)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


@router.delete("/{agent_id}", response_model=AgentData)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = crud.delete_agent(db, agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent