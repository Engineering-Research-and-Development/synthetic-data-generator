from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from model_registry.validation.valschema import CreateDataType
from ..dependencies import SessionDep
from model_registry.database.handlers import dt_handler as db_handler
from model_registry.validation.handlers import dt_valhander

router = APIRouter(prefix="/datatypes")

@router.get("/", status_code=200)
async def get_all_datatypes(session: SessionDep):
    return db_handler.get_all(session)

@router.get("/{data_id}", status_code=200)
async def get_all_datatypes(data_id: int, session: SessionDep):
    try:
        datatype = db_handler.get_by_id(data_id,session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No datatype with this id has been found")
    return datatype

@router.post("/", status_code=201)
async def create_datatype(datatype: CreateDataType, session: SessionDep):
    validated_datatype = dt_valhander.validate_model(datatype)
    if not db_handler.is_datatype_present(validated_datatype, session):
        db_handler.save_model(validated_datatype,session,refresh=True)
    else:
        raise HTTPException(status_code=400, detail="Datatype is already present in model registry")
    return {"message": "Created this new datatype with id", "id": str(validated_datatype.id)}

@router.delete("/{datatypes_id}", status_code=200)
async def delete_datatype(datatypes_id: int, session: SessionDep):
    try:
        datatype = db_handler.get_by_id(datatypes_id,session)
        session.delete(datatype)
        session.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No datatype with this id has been found")