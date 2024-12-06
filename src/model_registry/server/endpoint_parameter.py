import peewee
from model_registry.server import service
from model_registry.server.validation import TypeAdapter,\
    ParameterIn, ModifyParameter, ParameterOut
from fastapi import HTTPException
from typing import List

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

