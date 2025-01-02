"""This module implements the business logic for system models"""
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from model_registry.database.schema import SystemModel, AllowedDataType,DataType
from model_registry.database.model import engine,Session
from sqlmodel import select, join, SQLModel


def get_models_and_datatype() -> list[SQLModel]:
    with Session(engine) as session:
        statement = select(SystemModel,DataType.type,DataType.is_categorical).\
            join(AllowedDataType,onclause=SystemModel.name == AllowedDataType.algorithm_name).\
            join(DataType)
        results = session.exec(statement).all()
    return results