from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.validation.schema import CreateAlgorithm,Algorithm as PydanticAlgorithm, CreateAllowedData\
    ,AlgorithmAndAllowedDatatypes
from database.schema import DataType, AllowedDataType, db, Algorithm, TrainedModel

from routers.trained_models import delete_train_model

from peewee import DoesNotExist,IntegrityError,fn,JOIN

router = APIRouter(prefix="/algorithms")


@router.post("/",
             status_code=201,
             name="Create a new algorithm",
             summary="It creates an algorith  given the all the information and allowed datatypes",
             responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}}
             )
async def add_algorithm_and_datatype(algorithm: CreateAlgorithm, allowed_data: list[CreateAllowedData]):
    with db.atomic() as transaction:
        try:
            saved_algo = Algorithm.create(**algorithm.model_dump())
        except IntegrityError:
            return JSONResponse(status_code=500, content={'message': "Error in processing the request"})
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
            description="It returns all the algorithms present in the model registry")
async def get_all_algorithms() -> list[PydanticAlgorithm]:
    results = [PydanticAlgorithm(**sys_model) for sys_model in Algorithm.select().dicts()]
    return results

@router.get("/allowed_datatypes",
            status_code=200,
            name="Get all algorithms and allowed datatypes",
            summary="It returns all the algorithmss with their respective allowed datatypes in the model registry")
async def get_all_algorithms_datatypes() -> list[AlgorithmAndAllowedDatatypes]:
    query = (Algorithm.select(
        Algorithm,fn.JSON_AGG(fn.JSON_BUILD_OBJECT('datatype',DataType.type,'is_categorical',DataType.is_categorical))
    .alias("allowed_data"))
             .join(AllowedDataType,JOIN.LEFT_OUTER)
             .join(DataType,JOIN.LEFT_OUTER)
             .group_by(Algorithm.id))
    return [AlgorithmAndAllowedDatatypes(**row) for row in query.dicts()]


@router.get("/{algorithm_id}",
            status_code=200,
            name="Get algorithm by id",
            summary="It returns an algorithm given the id",
            responses={404: {"model": str}},
            response_model=PydanticAlgorithm)
async def get_algorithm_by_id(algorithm_id: int):
    try:
        sys_model = Algorithm.select().where(Algorithm.id == algorithm_id).dicts().get()
    except DoesNotExist:
        return JSONResponse(status_code=404,content={"message":"Algorithm not found"})
    return PydanticAlgorithm(**sys_model)

@router.get("/{algorithm_id}/allowed_datatypes",
            status_code=200,
            name="Get algorithm by id and his allowed datatypes",
            summary="It returns a algorithm given the id and his allowed datatypes",
            responses={404: {"model": str}},
            response_model=AlgorithmAndAllowedDatatypes)
async def get_algorithm_by_id_and_datatypes(algorithm_id: int):
    try:
        algorithm = (Algorithm.select(
            Algorithm,fn.JSON_AGG(fn.JSON_BUILD_OBJECT('datatype',DataType.type,'is_categorical',DataType.is_categorical))
        .alias("allowed_data"))
                 .join(AllowedDataType,JOIN.LEFT_OUTER)
                 .join(DataType,JOIN.LEFT_OUTER)
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
    try:
        algorithm = Algorithm.get_by_id(algorithm_id)
    except DoesNotExist:
        return JSONResponse(status_code=404,content={"message":"This algorithm does not exist!"})
    # First we delete the allowed datatypes
    AllowedDataType.delete().where(AllowedDataType.algorithm_id == algorithm_id).execute()
    # Then we delete all the train models associated with it
    trained_model_ids = TrainedModel.select(TrainedModel.id).where(TrainedModel.algorithm_id == algorithm_id).dicts()
    for row in trained_model_ids:
        await delete_train_model(row['id'])
    # Finally we delete the algorithm
    algorithm.delete_instance()