from model_registry.server.dependencies import SessionDep
from model_registry.database.schema import DataType
from sqlmodel import select

def get_id_by_type_and_categorical(datatype: str, is_categorical: bool,session:SessionDep):
    statement = select(DataType.id).where(DataType.type == datatype) \
        .where(DataType.is_categorical == is_categorical)
    result = session.exec(statement).one()
    return result


def is_datatype_present(datatype: DataType, session: SessionDep) -> bool:
    statement = select(DataType.id).where(datatype.type == DataType.type)\
        .where(datatype.is_categorical == DataType.is_categorical)
    result = session.exec(statement).all()
    if len(result) == 0:
        return False
    else:
        return True

def get_all(session: SessionDep) -> list[DataType]:
    statement = select(DataType)
    results = session.exec(statement)
    return results.all()

def get_by_id(datatype_id: int,session: SessionDep):
    statement = select(DataType).where(DataType.id == datatype_id)
    datatype = session.exec(statement).one()
    return datatype

def save_model(model: DataType,session: SessionDep, refresh: bool = False) -> None:
    session.add(model)
    session.commit()
    if refresh:
        session.refresh(model)