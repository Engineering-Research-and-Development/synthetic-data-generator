from fastapi import APIRouter, HTTPException
from model_registry.database import model
import sqlalchemy
from model_registry.database.schema import SystemModel
from model_registry.server.validation import CreateSystemModel
from model_registry.server.service import sm_service
from sqlalchemy.exc import  NoResultFound

router = APIRouter()


@router.post("/system_models",status_code=201)
async def add_trained_model(create_model: CreateSystemModel):
    """
    Given a System Model it saves it to the repository. A valid System Model must have a unique name, a description
    and a loss function
    :param create_model: A System Model passed in the body of the POST request
    :return:
    """
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
    """
    This function returns all system models as well as their allowed data type
    :return:
    """
    models = sm_service.get_models_and_datatype()
    # Creating a more structured payload
    payload = [{"name":model.name,"description":model.description,"loss_function":model.loss_function
                   ,"allowed_datatype":datatype,"categorical":categorical} for model,datatype,categorical in models]
    return payload

@router.get("/system_models/{system_model_id}",status_code=200)
async def get_system_model_by_id(system_model_id: int):
    """
    This function given a system model id it returns it
    :param system_model_id: Integer. A System model it
    :return: A system model
    :raise: 404 if the system model is not found
    """
    try:
        system_model = model.select_data_by_id(SystemModel,system_model_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No system model with id: " + str(system_model_id) + " has been found")
    return system_model


@router.delete("/system_models/{system_model_id}",status_code=200)
async def delete_system_model(system_model_id: int):
    """
    Given a system model id, it deletes it
    :param system_model_id: Integer. A system model id
    :return:
    """
    try:
        model.delete_data_by_id(SystemModel,system_model_id)
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail="No system model with id: " + str(system_model_id) + " has been found")