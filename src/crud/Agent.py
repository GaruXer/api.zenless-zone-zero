from sqlalchemy.orm import Session

from models.Agent import Agent
from schemas.Agent import AgentBase

def create_agent(db: Session, agent: AgentBase):
    agent = Agent(**agent.model_dump())

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


def get_all_agents(db: Session):
    return db.query(Agent).all()


def get_agent(db: Session, agent_id: int):
    return db.query(Agent).filter(Agent.id == agent_id).first()


def update_agent(db: Session, agent_id: int, updated_agent: AgentBase):
    agent = get_agent(db, agent_id)

    if agent:
        for key, value in updated_agent.model_dump().items():
            setattr(agent, key, value)

        db.commit()
        db.refresh(agent)

    return agent


def delete_agent(db: Session, agent_id: int):
    agent = get_agent(db, agent_id)

    if agent:
        db.delete(agent)
        db.commit()

    return agent