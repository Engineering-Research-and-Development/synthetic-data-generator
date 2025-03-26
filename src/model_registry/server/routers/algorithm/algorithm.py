from fastapi import APIRouter
from peewee import DoesNotExist, IntegrityError, fn, JOIN
from starlette.responses import JSONResponse

from server.database.schema import DataType, AlgorithmDataType, Algorithm
from server.database.validation_schema import (
    Algorithm
)
from server.routers.algorithm.validation_schema import AlgorithmList

router = APIRouter(prefix="/algorithms", tags=["Algorithms"])


@router.post(
    "/",
    status_code=201,
    name="Create a new algorithm",
    summary="It creates an algorith given the all the information and allowed datatypes",
    responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}},
)
async def add_algorithm_and_datatype(
    algorithm: Algorithm, allowed_data: list[DataType]
):
    """
    This method lets the user add a new algorithm to the model registry. An algorithm name must be ***unique*** (error 400
    will be returned if not) and the datatypes must be ***already present*** in the model registry, otherwise an error will be
    returned and the user must add the new datatype it wants to use with POST /datatypes
    """
    with db.atomic() as transaction:
        saved_algo, _ = Algorithm.get_or_create(**algorithm.model_dump())
        for feature in allowed_data:
            try:
                datatype = (
                    DataType.select()
                    .where(DataType.type == feature.datatype)
                    .where(DataType.is_categorical == feature.is_categorical)
                    .get()
                )
            except DoesNotExist:
                transaction.rollback()
                return JSONResponse(
                    status_code=404,
                    content={
                        "message": "This datatype is currently not supported"
                        ", to use it add it with POST /datatype",
                        "datatype": {
                            "datatype": feature.datatype,
                            "is_categorical": feature.is_categorical,
                        },
                    },
                )
            try:
                AlgorithmDataType.insert(
                    datatype=datatype.id, algorithm_id=saved_algo.id
                ).execute()
            except IntegrityError:
                transaction.rollback()
                return JSONResponse(
                    status_code=500,
                    content={"message": "Error in processing the request"},
                )

    return {"message": "Created algorithm with id", "id": str(saved_algo.id)}


@router.get(
    "/",
    status_code=200,
    name="Get all algorithms",
    response_model=AlgorithmList
)
async def get_all_algorithms():
    """
    This method returns all the algorithms that are present in the model registry.
    """
    algorithms = Algorithm.select().dicts()
    return AlgorithmList(algorithms=algorithms)



@router.get(
    "/{algorithm_id}",
    status_code=200,
    name="Get algorithm by id",
    summary="It returns an algorithm given the id",
    responses={404: {"model": str}}
)
async def get_algorithm_by_id(
    algorithm_id: int
):
    """
    Given an id, this method returns a specific algorithm. The query parameter `include_allowed_datatypes` (default ***False***)
    dictates if the method must return the associated allowed datatypes of the request algorithm
    """
    pass



@router.delete(
    "/{algorithm_id}",
    status_code=200,
    name="Delete an algorithm given his id",
    summary="It deletes an algorithm given the id and his allowed datatypes and trained models",
    responses={404: {"model": str}},
)
async def delete_algorithm(algorithm_id: int):
    """
    Given an id, this method deletes an algorithm and all the allowed datatypes as well as trained models, training info
    and feature schema
    """
    Algorithm.delete_by_id(algorithm_id)
