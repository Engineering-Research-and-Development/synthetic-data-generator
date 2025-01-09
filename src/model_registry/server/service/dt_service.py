from sqlmodel import select, join
from model_registry.database.schema import DataType
from model_registry.database.model import engine,Session

def is_datatype_present(datatype: DataType) -> bool:
    with Session(engine) as session:
        statement = select(DataType.id).where(datatype.type == DataType.type)\
            .where(datatype.is_categorical == DataType.is_categorical)
        result = session.exec(statement).all()
    if len(result) == 0:
        return False
    else:
        return True