from fastapi import APIRouter, HTTPException
from pydantic.v1 import validate_model

from model_registry.database import model
import sqlalchemy
from model_registry.database.schema import SystemModel, AllowedDataType
from model_registry.server.validation import CreateSystemModel, CreateDataType
from model_registry.server.service import sm_service as service
from sqlalchemy.exc import  NoResultFound,IntegrityError

router = APIRouter()


@router.post("/system_models",status_code=201)
async def add_system_model_and_datatype(system_model: CreateSystemModel,data_types: list[CreateDataType]):
    """
    Given a System Model it saves it to the repository. A valid System Model must have a unique name, a description
    and a loss function
    :param create_model: A System Model passed in the body of the POST request
    :param: data_types: A list of datatypes that the system model uses. They will be checked if present in the repository
    and if so they will be allowed
    :return:
    """
    try:
        # First validate input
        validated_model = SystemModel.model_validate(system_model)
    except sqlalchemy.exc.StatementError:
        raise HTTPException(status_code=400,detail="System model data passed is not correctly formatted. Check /docs to ensure"
                                                   " that the input is presented correctly")
    validated_data_types = service.validate_all_data_types(data_types)
    # If the datatype passed by the user are valid then we save the model and we add them to the AllowedDatatypesTable
    if service.are_datatypes_allowed(validated_data_types):
        try:
            model.save_data(validated_model, refresh_data=True)
        except IntegrityError:
            raise HTTPException(status_code=400,
                                detail="System Model must be unique. The name passed is already present in the registry")
        for datatype in validated_data_types:
            model.save_data(AllowedDataType(algorithm_name=validated_model.name,datatype=datatype.id))
    else:
        raise HTTPException(status_code=400,detail="The provided datatypes are not currently allowed. You need to add them "\
                                                   "explicitly with POST /data_types")

    return {"message":"Created system model with name","name":str(validated_model.name)}


# Add a new model to the repository
@router.get("/system_models",status_code=201)
async def get_all_system_models():
    """
    This function returns all system models as well as their allowed data type
    :return:
    """
    models = service.get_models_and_datatype()
    # Creating a more structured payload
    payload = [{"name":model["name"],"description":model["description"],"loss_function":model["loss_function"]
                   ,"allowed_datatype":model["allowed_datatype"],"categorical":model["categorical"]} for model in models]
    return payload

# TODO: Further test must be conducted here
@router.get("/system_models/{system_model_name}",status_code=200)
async def get_system_model_by_name(system_model_name: str):
    """
    This function given a system model id it returns it
    :param system_model_id: Integer. A System model it
    :return: A system model
    :raise: 404 if the system model is not found
    """
    system_model = service.get_model_by_name(system_model_name)
    return system_model


@router.delete("/system_models/{system_model_name}",status_code=200)
async def delete_system_model(system_model_name: str):
    """
    Given a system model id, it deletes it
    :param system_model_id: Integer. A system model id
    :return:
    """
    # We get it so we check it exists
    system_model = await get_system_model_by_name(system_model_name)
    allowed_data_types = service.get_model_allowed_datatypes()
    for data in allowed_data_types:
        model.delete_instance(data)
    model.delete_instance(system_model)

