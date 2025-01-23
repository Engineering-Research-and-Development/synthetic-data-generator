from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from model_registry.database.schema import TrainingInfo
from ..dependencies import SessionDep

router = APIRouter(prefix="/training_info")

@router.get("/{training_info_id}", status_code=200)
async def get_trained_info(training_info_id: int, session: SessionDep):
    try:
        statement = select(TrainingInfo).where(TrainingInfo.id == training_info_id)
        train_info = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No training info with id: " + str(training_info_id) + " has been found")
    return train_info

@router.delete("/{training_info_id}", status_code=200)
async def delete_training_info(training_info_id: int, session: SessionDep):
    train_info = await get_trained_info(training_info_id)
    session.delete(train_info)
    session.commit()