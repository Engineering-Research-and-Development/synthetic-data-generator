from model_registry.server.dependencies import SessionDep
from model_registry.database.schema import TrainingInfo
from sqlmodel import select


def save_model(model: TrainingInfo,session: SessionDep, refresh: bool = False) -> None:
    session.add(model)
    session.commit()
    if refresh:
        session.refresh(model)


def get_by_id(train_id: int, session: SessionDep):
    statement = select(TrainingInfo).where(TrainingInfo.id == train_id)
    training_info = session.exec(statement).one()
    return training_info