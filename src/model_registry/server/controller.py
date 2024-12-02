import peewee
from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
from typing import List

from model_registry.server import service
from model_registry.server.validation import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPI application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
    yield
    #  This part is done after the FASTAPI application is run


# Program entry point
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def helloworld():
    return {'message':'Hello world'}


@app.post("/models",status_code=201)
async def create_model(input_model: MlModelIn):
    # First step: check if the Algorithm id is valid
    try:
        # TODO: This could be changed so that the whole algorithm can be passed for model creation instead of
        #  retrieving it
        algorithm = service.get_algorithm_by_id(input_model.algorithm)
        service.create_model(input_model, algorithm)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail='An algorithm with id ' + str(input_model.algorithm) + ' does not exist!')
    except peewee.IntegrityError:
        raise HTTPException(status_code=400,detail="A model with the name passed already exists. Model's name must"
                                                   " be unique")

@app.get("/models",status_code=200)
# TODO: I suspect the pydantic validation causes a N + 1 query to validate the data. This is not
#  optimal and should be fixed - Chiedi a Fabio
async def get_models():
        return TypeAdapter(List[MlModelOut]).validate_python(service.get_all_models())


@app.get("/models/{model_id}",status_code=200)
async def get_algorithm(model_id: int):
    try:
            model = service.get_model_by_id(model_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="A model with this id has not been found!")
    return TypeAdapter(MlModelOut).validate_python(model)


@app.put("/models/{model_id}",status_code=200)
async def update_model(model_id: int,update_data: ModifyMlModel):
    try:
        return service.update_model(model_id, update_data)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="A model with this id does not exist!")


@app.delete("/models/{model_id}",status_code=200)
async def delete_model(model_id: int):
    try:
        service.delete_model(model_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="A model with this id does not exist!")



# CRUD for Algorithms
@app.post("/algorithms",status_code=201)
async def create_algorithm(input_algorithm: AlgorithmIn):
    service.create_algorithm(input_algorithm)

@app.get("/algorithms",status_code=200)
async def get_algorithms():
    return TypeAdapter(List[AlgorithmOut]).validate_python(service.get_all_algorithms())

@app.get("/algorithms/{algorithm_id}",status_code=200)
async def get_algorithm(algorithm_id: int):
    try:
            algorithm = service.get_algorithm_by_id(algorithm_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="An algorithm with this id has not been found!")
    return TypeAdapter(AlgorithmOut).validate_python(algorithm)

@app.put("/algorithms/{algorithm_id}",status_code=200)
async def update_algorithm(algorithm_id: int,update_data: AlgorithmIn):
    try:
        service.update_algorithm(algorithm_id, update_data)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="An algorithm with this id has not been found!")

@app.delete("/algorithms/{algorithm_id}",status_code=200)
async def delete_algorithm(algorithm_id: int):
    try:
        service.delete_algorithm(algorithm_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="An algorithm with this id does not exist!")


# CRUD for Parameter
@app.post("/parameters",status_code=201)
async def create_parameter(input_param: ParameterIn):
    service.create_parameter(input_param)

@app.get("/parameters",status_code=200)
async def get_parameters():
    return TypeAdapter(List[ParameterOut]).validate_python(service.get_all_parameters())

@app.get("/parameters/{parameter_id}",status_code=200)
async def get_parameter(parameter_id: int):
    try:
            param = service.get_parameter_by_id(parameter_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="A parameter with this id has not been found!")
    return TypeAdapter(ParameterOut).validate_python(param)

@app.put("/parameters/{parameter_id}",status_code=200)
async def update_parameter(parameter_id: int,update_data: ModifyParameter):
    try:
        service.update_parameter(parameter_id, update_data)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="A parameter with this id has not been found!")

@app.delete("/parameters/{parameter_id}",status_code=200)
async def delete_parameter(parameter_id: int):
    try:
        service.delete_parameter(parameter_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="A parameter with this id does not exist!")


# CRUD for ModelParameter
@app.post("/model_parameters",status_code=201)
async def create_model_parameter(input_model_param: ModelParameterIn):
    # Get model and parameter
    try:
        model = service.get_model_by_id(input_model_param.model)
        param = service.get_parameter_by_id(input_model_param.parameter)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="The model or param with the passed ids have not been found")
    service.create_model_parameter(input_model_param, model, param)

@app.get("/model_parameters",status_code=200)
async def get_model_parameters():
    return TypeAdapter(List[ModelParameterOut]).validate_python(service.get_all_model_parameters())

@app.get("/model_parameters/{model_param_id}",status_code=200)
async def get_model_parameter(model_param_id: int):
    try:
            model_param = service.get_model_parameter_by_id(model_param_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="A model parameter with this id has not been found!")
    return TypeAdapter(ModelParameterOut).validate_python(model_param)

@app.put("/model_parameters/{model_param_id}",status_code=200)
async def update_model_parameter(model_param_id: int,update_data: ModifyModelParameter):
    try:
        service.update_model_parameter(model_param_id, update_data)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="A model parameter with this id has not been found!")

@app.delete("/model_parameters/{model_param_id}",status_code=200)
async def delete_model_parameter(model_param_id: int):
    try:
        service.delete_model_parameter(model_param_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="A model parameter with this id does not exist!")