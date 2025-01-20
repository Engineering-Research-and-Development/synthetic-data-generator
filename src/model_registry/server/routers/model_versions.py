from fastapi import APIRouter, HTTPException,Depends
from model_registry.database.schema import ModelVersion
from model_registry.database import model
from sqlalchemy.exc import  NoResultFound
from model_registry.database.validation import ValidHeaders

router = APIRouter()


@router.get("/versions/{version_id}",status_code=200)
async def get_version_by_id(version_id: int):
    """
    Given an model version's id, it will return it
    :param version_id: Integer. A model version id
    :return: The version of a trained model
    """
    try:
        version = model.select_data_by_id(ModelVersion,version_id)
    except NoResultFound:
        raise HTTPException(status_code=404,detail="No version with id: " + str(version_id) + " has been found")
    return version


@router.get("/versions",status_code=200)
async def get_all_model_versions():
    """
    It returns all the versions of all the trained models
    :return:
    """
    return model.select_all(ModelVersion)
