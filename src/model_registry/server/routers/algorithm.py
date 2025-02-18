from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from database.validation.schema import CreateAlgorithm,Algorithm as PydanticAlgorithm, CreateAllowedData\
    ,AlgorithmAndAllowedDatatypes
from database.schema import DataType, AllowedDataType, db, Algorithm, TrainedModel

from routers.trained_models import delete_train_model

from peewee import DoesNotExist,IntegrityError,fn,JOIN

router = APIRouter(prefix="/algorithms", tags=['Algorithms'])


@router.post("/",
             status_code=201,
             name="Create a new algorithm",
             summary="It creates an algorith given the all the information and allowed datatypes",
             responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}}
             )
async def add_algorithm_and_datatype(algorithm: CreateAlgorithm, allowed_data: list[CreateAllowedData]):
    """
    This method lets the user add a new algorithm to the model registry. An algorithm name must be ***unique*** (error 400
    will be returned if not) and the datatypes must be ***already present*** in the model registry, otherwise an error will be
    returned and the user must add the new datatype it wants to use with POST /datatypes
    """
    with db.atomic() as transaction:
        try:
            saved_algo = Algorithm.create(**algorithm.model_dump())
        except IntegrityError:
            return JSONResponse(status_code=400, content={'message': "Algorithm names must be uniques! Try another name!"})
        for feature in allowed_data:
            try:
                datatype = DataType.select().where(DataType.type == feature.datatype) \
                    .where(DataType.is_categorical == feature.is_categorical).get()
            except DoesNotExist:
                transaction.rollback()
                return JSONResponse(status_code=400,content={"message":"The datatype is currently not supported"
                                                                              ", to use it add it with POST /datatype"})
            try:
                AllowedDataType.insert(datatype=datatype.id, algorithm_id=saved_algo.id).execute()
            except IntegrityError:
                transaction.rollback()
                return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

    return {"message": "Created algorithm with id", "id": str(saved_algo.id)}

@router.get("/",
            status_code=200,
            name="Get all algorithms",
            response_model=list[PydanticAlgorithm] | list[AlgorithmAndAllowedDatatypes])
async def get_all_algorithms(include_allowed_datatypes: bool | None = Query(description="Include the allowed datatypes"
                              "for each algorithm present in the system",default=False)):

    """
        This method returns all the algorithms that are present in the model registry. The query parameter
        `include_allowed_datatypes` (default ***False***) if ***True*** will let the model registry return for each
        algorithm the list of allowed datatypes it deals with
    """
    if not include_allowed_datatypes:
        results = [PydanticAlgorithm(**sys_model) for sys_model in Algorithm.select().dicts()]
        return results
    else:
        query = (Algorithm.select(
            Algorithm,
            fn.JSON_AGG(fn.JSON_BUILD_OBJECT('datatype', DataType.type, 'is_categorical', DataType.is_categorical))
            .alias("allowed_data"))
                 .join(AllowedDataType, JOIN.LEFT_OUTER)
                 .join(DataType, JOIN.LEFT_OUTER)
                 .group_by(Algorithm.id))
        return [AlgorithmAndAllowedDatatypes(**row) for row in query.dicts()]



@router.get("/{algorithm_id}",
            status_code=200,
            name="Get algorithm by id",
            summary="It returns an algorithm given the id",
            responses={404: {"model": str}},
            response_model=PydanticAlgorithm | AlgorithmAndAllowedDatatypes)
async def get_algorithm_by_id(algorithm_id: int,
                              include_allowed_datatypes: bool | None = Query(description="Include the allowed datatypes"
                              "for each algorithm present in the system",default=False)):
    """
    Given an id, this method returns a specific algorithm. The query parameter `include_allowed_datatypes` (default ***False***)
    dictates if the method must return the associated allowed datatypes of the request algorithm
    """
    if not include_allowed_datatypes:
        try:
            sys_model = Algorithm.select().where(Algorithm.id == algorithm_id).dicts().get()
        except DoesNotExist:
            return JSONResponse(status_code=404,content={"message":"Algorithm not found"})
        return PydanticAlgorithm(**sys_model)
    else:
        try:
            algorithm = (Algorithm.select(
                Algorithm,
                fn.JSON_AGG(fn.JSON_BUILD_OBJECT('datatype', DataType.type, 'is_categorical', DataType.is_categorical))
                .alias("allowed_data"))
                         .join(AllowedDataType, JOIN.LEFT_OUTER)
                         .join(DataType, JOIN.LEFT_OUTER)
                         .where(Algorithm.id == algorithm_id)
                         .group_by(Algorithm.id)).dicts().get()
        except DoesNotExist:
            return JSONResponse(status_code=404, content={'message': "Algorithm not present"})
        return AlgorithmAndAllowedDatatypes(**algorithm)



@router.delete("/{algorithm_id}",
               status_code=200,
               name="Delete an algorithm given his id",
               summary="It deletes an algorithm given the id and his allowed datatypes and trained models",
               responses={404: {"model": str}})
async def delete_algorithm(algorithm_id: int):
    """
    Given an id, this method deletes an algorithm and all the allowed datatypes as well as trained models, training info
    and feature schema
    """
    try:
        algorithm = Algorithm.get_by_id(algorithm_id)
    except DoesNotExist:
        return JSONResponse(status_code=404,content={"message":"This algorithm does not exist!"})

    algorithm.delete_instance()
