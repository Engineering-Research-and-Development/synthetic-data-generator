"""This module implements the business logic for system models"""
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound,StatementError

from model_registry.database.schema import SystemModel, AllowedDataType,DataType
from model_registry.database.model import engine,Session
from sqlmodel import select, join, SQLModel


def get_models_and_datatype() -> list:
    with Session(engine) as session:
        statement = select(SystemModel,DataType.type,DataType.is_categorical).\
            join(AllowedDataType,onclause=SystemModel.name == AllowedDataType.algorithm_name).\
            join(DataType)
        results = session.exec(statement).all()
    payload = {}
    for result in results:
        model = payload.get(result[0].name)
        if model is None:
            payload.update({result[0].name: {"name": result[0].name,
                                           "description": result[0].description,
                                           "loss_function": result[0].loss_function,
                                           "allowed_datatype": [result[1]],
                                           "categorical": [result[2]]}})
        else:
            model["allowed_datatype"].append(result[1])
            model["categorical"].append(result[2])
    return list(payload.values())


def validate_all_data_types(datatypes: list[SQLModel]) -> list[SQLModel]:
    payload = []
    for data in datatypes:
        try:
            payload.append(DataType.model_validate(data))
        except StatementError:
            raise HTTPException(status_code=400,
                                detail="The passed datatype is not correct. Check /docs")
    return payload




def save_allowed_datatype(data):

    with Session(engine) as session:
        for data in unique.values():
            # Then we check if it is in the database
            statement = select(DataType.id).where(DataType.type == data.type)
            try:
                result = session.exec(statement).one()
            except NoResultFound:
                raise HTTPException(status_code=400,
                                    detail="This kind of datatype is not supported. Please add it to use it")
            # We then add the datatype to the Allowed Data Type Relationship



