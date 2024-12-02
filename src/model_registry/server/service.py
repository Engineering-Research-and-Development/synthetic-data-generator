"""This module implements all the database operations offered by the model registry module. """

import peewee
from fastapi import HTTPException

from model_registry.database.model import database, tables, Algorithm, MlModel, Parameter, ModelParameter
from model_registry.server.validation import MlModelIn, ModifyMlModel, AlgorithmIn, ParameterIn, ModelParameterIn, \
    ModifyParameter, ModifyModelParameter


# Utils method for resetting the db
@database.connection_context()
def drop_all_tables() -> None:
    database.drop_tables(tables)

@database.connection_context()
def create_all_tables() -> None:
    database.create_tables(tables)

@database.connection_context()
def reset_database() -> None:
    drop_all_tables()
    create_all_tables()


# CRUD for models
@database.connection_context()
def create_model(model: MlModelIn,algorithm: Algorithm):
    MlModel.create(
        name=model.name,description=model.description,status = model.status,
    version = model.version,image = model.image, input_shape = model.input_shape,
    dtype = model.dtype,algorithm = algorithm
    )

@database.connection_context()
def create_models(models: list[MlModel]) -> None:
        MlModel.bulk_create(models)

@database.connection_context()
def get_all_models() -> list[MlModel]:
    return list(MlModel.select())

@database.connection_context()
def get_model_by_id(id: int) -> MlModel:
    return MlModel.get(MlModel.id == id)

@database.connection_context()
def update_model(model_id: int,update_data: ModifyMlModel):
    # Getting all the fields that are not None and we want to update
    # Why did we do this? Because in this way we can have any param that is valid to be update automatically
    # without writing a bunch of if and else
    x = {k: v for k, v in vars(update_data).items() if v is not None}
    # For reference see: https://stackoverflow.com/questions/39310191/peewee-update-an-entry-with-a-dictionary
    if MlModel.update(**x).where(MlModel.id == model_id).execute() == 0:
        raise HTTPException(status_code=400,detail="Update data is the same as original data or no model exists with"
                                                   " that id")

@database.connection_context()
def delete_model(model_id: int):
    model = get_model_by_id(model_id)
    model.delete_instance()


# CRUD for algorithms
@database.connection_context()
def create_algorithm(algorithm: AlgorithmIn) -> None:
    Algorithm.create(name=algorithm.name)

@database.connection_context()
def create_algorithms(algorithms: list[Algorithm]) -> None:
    Algorithm.bulk_create(algorithms)

@database.connection_context()
def get_algorithm_by_id(algorithm_id: int) -> Algorithm:
    return Algorithm.get(Algorithm.id == algorithm_id)

@database.connection_context()
def get_all_algorithms() -> list[Algorithm]:
    return list(Algorithm.select())

@database.connection_context()
def update_algorithm(algorithm_id: int,update_data: AlgorithmIn):
    if Algorithm.update(name=update_data.name).where(Algorithm.id == algorithm_id).execute() == 0:
        raise HTTPException(status_code=400,detail="Update data is the same as original data or no algorithm exists with"
                                                   " that id")

@database.connection_context()
def delete_algorithm(algorithm_id: int):
    algorithm = get_algorithm_by_id(algorithm_id)
    algorithm.delete_instance()


# CRUD for parameters
@database.connection_context()
def create_parameter(param: ParameterIn) -> None:
    Parameter.create(param_name=param.param_name,param_description=param.param_description,dtype=param.dtype)

@database.connection_context()
def create_parameters(params: list[Parameter]) -> None:
    Parameter.bulk_create(params)

@database.connection_context()
def get_parameter_by_id(param_id: int) -> Parameter:
    return Parameter.get(Parameter.id == param_id)

@database.connection_context()
def get_all_parameters() -> list[Parameter]:
    return list(Parameter.select())

@database.connection_context()
def update_parameter(param_id: int,update_data: ModifyParameter):
    # See update_model for an explanation
    x = {k: v for k, v in vars(update_data).items() if v is not None}
    if Parameter.update(**x).where(Parameter.id == param_id).execute() == 0:
        raise HTTPException(status_code=400,detail="Update data is the same as original data or no parameter exists with"
                                                   " that id")

@database.connection_context()
def delete_parameter(param_id: int):
    param = get_parameter_by_id(param_id)
    param.delete_instance(recursive=True)


# CRUD for model parameter
@database.connection_context()
def create_model_parameter(data_in: ModelParameterIn,model,param) -> None:
    ModelParameter.create(model=model,parameter=param,parameter_value=data_in.parameter_value,
                          max_threshold=data_in.max_threshold,min_threshold=data_in.min_threshold)

@database.connection_context()
def create_model_parameters(params: list[ModelParameter]) -> None:
    ModelParameter.bulk_create(params)

@database.connection_context()
def get_model_parameter_by_id(param_id: int) -> Parameter:
    return ModelParameter.get(ModelParameter.id == param_id)

@database.connection_context()
def get_all_model_parameters() -> list[ModelParameter]:
    return list(ModelParameter.select())

@database.connection_context()
def update_model_parameter(param_id: int,update_data: ModifyModelParameter):
    # See update_model for an explanation
    x = {k: v for k, v in vars(update_data).items() if v is not None}
    if ModelParameter.update(**x).where(ModelParameter.id == param_id).execute() == 0:
        raise HTTPException(status_code=400,detail="Update data is the same as original data or no model parameter"
                                                   " exists with that id")

@database.connection_context()
def delete_model_parameter(param_id: int):
    param = get_model_parameter_by_id(param_id)
    param.delete_instance()




