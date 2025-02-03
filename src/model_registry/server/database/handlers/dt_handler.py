from database.validation.schema import DataType as PydanticDataType
from database.schema import DataType

def get_id_by_type_and_categorical(datatype: str, is_categorical: bool) -> DataType:
    obj = DataType.select().where(DataType.type == datatype) \
        .where(DataType.is_categorical == is_categorical).get()
    return obj
#
#
# def is_datatype_present(datatype: DataType, session: SessionDep) -> bool:
#     statement = select(DataType.id).where(datatype.type == DataType.type)\
#         .where(datatype.is_categorical == DataType.is_categorical)
#     result = session.exec(statement).all()
#     if len(result) == 0:
#         return False
#     else:
#         return True
#
# def get_all(session: SessionDep) -> list[DataType]:
#     statement = select(DataType)
#     results = session.exec(statement)
#     return results.all()

def get_by_id(datatype_id: int) -> PydanticDataType:
    query = DataType.select().where(DataType.id == datatype_id)
    # This hack is done so that we can get a dictionary and unpack it into a pydantic model
    return [PydanticDataType(**row) for row in query.dicts()][0]


# def save_model(model: DataType,session: SessionDep, refresh: bool = False) -> None:
#     session.add(model)
#     session.commit()
#     if refresh:
#         session.refresh(model)