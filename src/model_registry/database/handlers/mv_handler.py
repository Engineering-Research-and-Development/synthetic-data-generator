from model_registry.server.dependencies import SessionDep
from model_registry.database.schema import ModelVersion
from sqlmodel import select

def save_model(model: ModelVersion,session: SessionDep, refresh: bool = False) -> None:
    session.add(model)
    session.commit()
    if refresh:
        session.refresh(model)

def get_all(session: SessionDep) -> list[ModelVersion]:
    statement = select(ModelVersion)
    results = session.exec(statement)
    return results.all()

def get_by_id(model_id: int,session: SessionDep):
    statement = select(ModelVersion).where(ModelVersion.id == model_id)
    model_version = session.exec(statement).one()
    return model_version