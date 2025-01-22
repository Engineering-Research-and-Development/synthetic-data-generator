from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from model_registry.database import model
from model_registry.database.schema import DataType
from model_registry.database.validation import CreateDataType
from model_registry.server.service import dt_service as service

router = APIRouter()


@router.get("/datatypes",status_code=200)
async def get_all_datatypes():
    return model.select_all(DataType)

@router.get("/datatypes/{data_id}",status_code=200)
async def get_all_datatypes(data_id: int):
    try:
        datatype = model.select_data_by_id(DataType,data_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No datatype with this id has been found")
    return datatype

@router.post("/datatypes",status_code=201)
async def create_datatype(datatype: CreateDataType):
    validated_datatype = DataType.model_validate(datatype)
    # We check that it is not present
    if not service.is_datatype_present(validated_datatype):
        model.save_data(validated_datatype,refresh_data=True)
    else:
        raise HTTPException(status_code=400,detail="Datatype is already present in model registry")
    return {"message":"Created this new datatype with id","id":str(validated_datatype.id)}

@router.delete("/datatypes/{datatypes_id}",status_code=200)
async def delete_datatype(datatypes_id: int):
    try:
        datatype = model.select_data_by_id(DataType,datatypes_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No datatype with this id has been found")
    model.delete_instance(datatype)

