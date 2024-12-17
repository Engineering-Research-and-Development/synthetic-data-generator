from fastapi import APIRouter, HTTPException
from model_registry.database.schema import ModelVersion
from ...database import model


router = APIRouter()

@router.get("/model_versions",status_code=201)
async def get_all_model_versions():
    return model.select_all(ModelVersion)

@router.get("/model_versions/{model_version_id}",status_code=201)
async def get_all_model_versions(model_version_id: int):
    return model.select_data_by_id(ModelVersion,model_version_id)
