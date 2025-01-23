import sqlalchemy
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from model_registry.database.schema import SystemModel, AllowedDataType
from model_registry.database.validation import CreateSystemModel, CreateDataType
from model_registry.server.errors import ValidationError
from ..dependencies import SessionDep
from model_registry.server.service import sm_service as service

router = APIRouter(prefix="/system_models")

@router.post("/", status_code=201)
async def add_system_model_and_datatype(system_model: CreateSystemModel, data_types: list[CreateDataType], session: SessionDep):
    try:
        validated_model = SystemModel.model_validate(system_model)
    except sqlalchemy.exc.StatementError:
        raise HTTPException(status_code=400, detail="System model data passed is not correctly formatted. Check /docs to ensure that the input is presented correctly")

    try:
        validated_data_types = service.validate_all_data_types(data_types, session)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="The provided datatypes are not currently allowed. You need to add them explicitly with POST /data_types")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    try:
        session.add(validated_model)
        session.commit()
        session.refresh(validated_model)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="System Model must be unique. The name passed is already present in the registry")

    for datatype in validated_data_types:
        session.add(AllowedDataType(algorithm_name=validated_model.name, datatype=datatype.id))
        session.commit()

    return {"message": "Created system model with name", "name": str(validated_model.name)}

@router.get("/", status_code=200)
async def get_all_system_models(session: SessionDep):
    models = service.get_models_and_datatype(session)
    payload = [{"name": model["name"], "description": model["description"], "loss_function": model["loss_function"], "allowed_datatype": model["allowed_datatype"], "is_categorical": model["categorical"]} for model in models]

    return payload

@router.get("/{system_model_name}", status_code=200)
async def get_system_model_by_name(system_model_name: str, session: SessionDep):
    try:
        system_model, types, is_categorical = service.get_model_by_name_and_datatypes(system_model_name, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No System Model has been found with this name!")
    return {"name": system_model.name, "description": system_model.description, "loss_function": system_model.loss_function, "allowed_datatype": types, "is_categorical": is_categorical}

@router.delete("/{system_model_name}", status_code=200)
async def delete_system_model(system_model_name: str, session: SessionDep):
    try:
        system_model, allowed_data_types = service.get_model_allowed_datatypes(system_model_name, session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="The system model either does not exist or has no allowed datatypes")

    for data in allowed_data_types:
        session.delete(data)
    session.delete(system_model)
    session.commit()