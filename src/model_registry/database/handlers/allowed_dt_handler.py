from model_registry.database.schema import AllowedDataType
from model_registry.server.dependencies import SessionDep

def create_object_and_save(algorithm_name: str,datatype_id: int,session: SessionDep) -> None:
    session.add(AllowedDataType(algorithm_name=algorithm_name, datatype=datatype_id))
    session.commit()

