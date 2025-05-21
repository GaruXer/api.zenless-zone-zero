from sqlalchemy.orm import Session

from src.models import Agent, Faction, Mindscape, Skill, SkillMultiplier, Stats, VoiceActor
from src.schemas.Agent import AgentBase

def create_agent(db: Session, agent: AgentBase):
    agent = Agent(
        name=agent.name,
        full_name=agent.full_name,
        rank=agent.rank,
        specialty=agent.specialty,
        attribute=agent.attribute,
        gender=agent.gender,
        faction=db.query(Faction).filter(Faction.name == agent.faction.name).first() or Faction(**agent.faction.model_dump()),
        height=agent.height,
        birthday=agent.birthday,
        version_released=agent.version_released,
        voice_actors=[VoiceActor(**voice_actor.model_dump()) for voice_actor in agent.voice_actors],
        base_stats=[Stats(**stats.model_dump()) for stats in agent.base_stats],
        skills=[Skill(name=skill.name, type=skill.type, description=skill.description, multipliers=[SkillMultiplier(**multiplier.model_dump()) for multiplier in skill.multipliers]) for skill in agent.skills],
        mindscapes=[Mindscape(**mindscape.model_dump()) for mindscape in agent.mindscapes]
    )

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
            if key in ["name", "full_name", "rank", "specialty", "attribute", "gender", "height", "birthday", "version_released"]:
                setattr(agent, key, value)

        agent.faction = db.query(Faction).filter(Faction.name == updated_agent.faction.name).first() or Faction(name=updated_agent.faction.name)

        db.query(VoiceActor).filter(VoiceActor.agent_id == agent_id).delete()
        agent.voice_actors = [VoiceActor(**voice_actor.model_dump()) for voice_actor in updated_agent.voice_actors]

        db.query(Stats).filter(Stats.agent_id == agent_id).delete()
        agent.base_stats = [Stats(**stats.model_dump()) for stats in updated_agent.base_stats]

        for skill in agent.skills:
            db.query(SkillMultiplier).filter(SkillMultiplier.skill_id == skill.id).delete()
        
        db.query(Skill).filter(Skill.agent_id == agent_id).delete()
        agent.skills=[Skill(name=skill.name, type=skill.type, description=skill.description, multipliers=[SkillMultiplier(**multiplier.model_dump()) for multiplier in skill.multipliers]) for skill in updated_agent.skills]

        db.query(Mindscape).filter(Mindscape.agent_id == agent_id).delete()
        agent.mindscapes = [Mindscape(**mindscape.model_dump()) for mindscape in updated_agent.mindscapes]

        db.commit()
        db.refresh(agent)

    return agent


def delete_agent(db: Session, agent_id: int):
    agent = get_agent(db, agent_id)

    if agent:
        db.delete(agent)
        db.commit()

    return agent


def create_or_update_agent(db: Session, agent: AgentBase):
    agent_in_db = db.query(Agent).filter_by(name = agent.name).first()

    if agent_in_db:
        update_agent(db, agent_in_db.id, agent)
    else:
        create_agent(db, agent)