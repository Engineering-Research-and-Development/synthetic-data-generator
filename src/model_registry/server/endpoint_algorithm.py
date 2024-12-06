import peewee
from model_registry.server import service
from model_registry.server.validation import  TypeAdapter,  \
    AlgorithmIn, AlgorithmOut
from fastapi import HTTPException
from typing import List

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

