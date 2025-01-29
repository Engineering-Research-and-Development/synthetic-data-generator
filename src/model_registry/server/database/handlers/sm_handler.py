from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from model_registry.database.schema import SystemModel, DataType, AllowedDataType
from model_registry.server.dependencies import SessionDep


def get_models_and_datatype(session: SessionDep) -> list:
    statement = select(SystemModel,DataType.type,DataType.is_categorical).\
        outerjoin(AllowedDataType,onclause=SystemModel.name == AllowedDataType.algorithm_name).\
        outerjoin(DataType)
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


def are_datatypes_allowed(datatypes, session: SessionDep):
    for data in datatypes:
        statement = select(DataType).where(DataType.type == data.type).where(DataType.is_categorical == data.is_categorical)
        results = session.exec(statement).all()
        if len(results) == 0:
            return False
    return True


def get_model_allowed_datatypes(model_name, session: SessionDep):
    statement = select(SystemModel,AllowedDataType).join(SystemModel).where(SystemModel.name == model_name)
    results = session.exec(statement).all()
    if len(results) == 0:
        raise NoResultFound
    allowed_datatypes = [x[1] for x in results]
    return results[0][0],allowed_datatypes


def get_model_by_name_and_datatypes(model_name: str, session: SessionDep):

    statement = select(SystemModel,AllowedDataType,DataType).join(AllowedDataType,onclause=SystemModel.name == AllowedDataType.algorithm_name)\
        .join(DataType).where(SystemModel.name == model_name)
    results = session.exec(statement).all()
    if len(results) == 0:
        raise NoResultFound
    types,is_categorical = [],[]
    for result in results:
        types.append(result[2].type)
        is_categorical.append(result[2].is_categorical)
    return results[0][0],types,is_categorical


def save_model(model: SystemModel,session: SessionDep, refresh: bool = False) -> None:
    session.add(model)
    session.commit()
    if refresh:
        session.refresh(model)
