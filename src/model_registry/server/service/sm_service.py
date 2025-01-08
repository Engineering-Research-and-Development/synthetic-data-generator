"""This module implements the business logic for system models"""
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound,StatementError

from model_registry.database.schema import SystemModel, AllowedDataType,DataType
from model_registry.database.model import engine,Session
from sqlmodel import select, join, SQLModel

from model_registry.test.trained_models.tm_unit_test import model


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
    with Session(engine) as session:
        for data in datatypes:
            statement = select(DataType.id).where(DataType.type == data.type).where(DataType.is_categorical == data.is_categorical)
            result = session.exec(statement).one()
            try:
                validated_data = DataType.model_validate(data)
            except StatementError:
                raise HTTPException(status_code=400,
                                    detail="The passed datatype is not correct. Check /docs")
            validated_data.id = result
            payload.append(validated_data)
    return payload

def are_datatypes_allowed(datatypes):
    with Session(engine) as session:
        for data in datatypes:
            statement = select(DataType).where(DataType.type == data.type).where(DataType.is_categorical == data.is_categorical)
            results = session.exec(statement).all()
            if len(results) == 0:
                return False
    return True

def get_model_allowed_datatypes(model_name):
    with Session(engine) as session:
            statement = select(AllowedDataType).where(SystemModel.name == model_name)
            result = session.exec(statement).all()
    if len(result) == 0:
        raise HTTPException(status_code=404,detail="The system model with name:" + model_name + "has no allowed datatypes")
    return result

def get_model_by_name(model_name: str):
    with Session(engine) as session:
        statement = select(SystemModel).where(SystemModel.name == model_name)
        result = session.exec(statement).all()
        if len(result) == 0:
            raise HTTPException(status_code=404,detail="No System Model has been found with this name!")
    return result