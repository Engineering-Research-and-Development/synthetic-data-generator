from model_registry.validation.valschema import CreateDataType
from model_registry.database.schema import DataType
from model_registry.database.handlers.dt_handler import get_id_by_type_and_categorical
from model_registry.server.dependencies import SessionDep
from model_registry.server.errors import ValidationError
from sqlalchemy.exc import StatementError

def validate_model(in_model: CreateDataType) -> DataType:
    return DataType.model_validate(in_model)


def validate_all_data_types(datatypes: list[CreateDataType], session: SessionDep) -> list[DataType]:
    payload = []
    for data in datatypes:
        datatype_id = get_id_by_type_and_categorical(data.type,data.is_categorical,session)
        try:
            validated_data = DataType.model_validate(data)
        except StatementError:
            raise ValidationError("The passed datatype is not correct. Check /docs")
        validated_data.id = datatype_id
        payload.append(validated_data)
    return payload
