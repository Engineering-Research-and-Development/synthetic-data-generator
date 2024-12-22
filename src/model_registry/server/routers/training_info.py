from fastapi import APIRouter, HTTPException
from model_registry.database import model
from model_registry.database.schema import TrainingInfo
from sqlalchemy.exc import NoResultFound

router = APIRouter()



@router.get("/training_info/{training_info_id}",status_code=200)
async def get_trained_info(training_info_id: int):
    try:
        train_info = model.select_data_by_id(TrainingInfo,training_info_id)
    except NoResultFound:
        raise HTTPException(status_code=404,detail="No training info with id: " +
                                                   str(training_info_id) + " has been found")
    return train_info



@router.delete("/training_info/{training_info_id}",status_code=200)
async def delete_training_info(training_info_id: int):
    train_info = await get_trained_info(training_info_id)
    model.delete_instance(train_info)