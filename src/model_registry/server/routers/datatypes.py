from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from model_registry.database.schema import DataType
from model_registry.database.validation import CreateDataType
from ..dependencies import SessionDep
from model_registry.server.service import dt_service as service

router = APIRouter(prefix="/datatypes")

@router.get("/", status_code=200)
async def get_all_datatypes(session: SessionDep):
    statement = select(DataType)
    results = session.exec(statement)
    return results.all()

@router.get("/{data_id}", status_code=200)
async def get_all_datatypes(data_id: int, session: SessionDep):
    try:
        statement = select(DataType).where(DataType.id == data_id)
        datatype = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No datatype with this id has been found")
    return datatype

@router.post("/", status_code=201)
async def create_datatype(datatype: CreateDataType, session: SessionDep):
    validated_datatype = DataType.model_validate(datatype)
    if not service.is_datatype_present(validated_datatype, session):
        session.add(validated_datatype)
        session.commit()
        session.refresh(validated_datatype)
    else:
        raise HTTPException(status_code=400, detail="Datatype is already present in model registry")
    return {"message": "Created this new datatype with id", "id": str(validated_datatype.id)}

@router.delete("/{datatypes_id}", status_code=200)
async def delete_datatype(datatypes_id: int, session: SessionDep):
    try:
        statement = select(DataType).where(DataType.id == datatypes_id)
        datatype = session.exec(statement).one()
        session.delete(datatype)
        session.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No datatype with this id has been found")