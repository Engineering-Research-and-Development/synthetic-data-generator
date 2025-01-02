from fastapi import APIRouter, HTTPException
from model_registry.database import model
import sqlalchemy
from model_registry.database.schema import SystemModel
from model_registry.server.validation import CreateSystemModel
from model_registry.server.service import sm_service

router = APIRouter()


@router.post("/system_models",status_code=201)
async def add_trained_model(create_model: CreateSystemModel):
    try:
        # First validate input
        validated_model = SystemModel.model_validate(create_model)
        # Then invoke the service to save the model
        model.save_data(validated_model)
    except sqlalchemy.exc.StatementError:
        raise HTTPException(status_code=400,detail="Data passed is not correctly formatted. Check /docs to ensure"
                                                   " that the input is presented correctly")


# Add a new model to the repository
@router.get("/system_models",status_code=201)
async def get_all_system_models():
    models = sm_service.get_models_and_datatype()
    # Creating a more structured payload
    payload = [{"name":model.name,"description":model.description,"loss_function":model.loss_function
                   ,"allowed_datatype":datatype,"categorical":categorical} for model,datatype,categorical in models]
    return payload

@router.get("/system_models/{system_model_id}",status_code=200)
async def get_system_model_by_id(system_model_id: int):
    return model.select_data_by_id(SystemModel,system_model_id)


@router.delete("/system_models/{system_model_id}",status_code=200)
async def delete_system_model(system_model_id: int):
    model.delete_data(SystemModel,system_model_id)
