from sqlmodel import select

from model_registry.database.schema import DataType
from model_registry.server.dependencies import SessionDep


def is_datatype_present(datatype: DataType, session: SessionDep) -> bool:
    statement = select(DataType.id).where(datatype.type == DataType.type)\
        .where(datatype.is_categorical == DataType.is_categorical)
    result = session.exec(statement).all()
    if len(result) == 0:
        return False
    else:
        return True