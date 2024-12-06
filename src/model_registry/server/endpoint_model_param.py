import peewee
from model_registry.server import service
from model_registry.server.validation import ModelParameterIn, ModelParameterOut, TypeAdapter, ModifyModelParameter
from fastapi import HTTPException
from typing import List


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