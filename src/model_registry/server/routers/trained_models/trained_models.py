import peewee
from fastapi import APIRouter, Path, Query
from starlette.responses import JSONResponse

from database.schema import (
    TrainedModel,
    ModelVersion,
    TrainModelDatatype,
    Algorithm,
    DataType,
)
from routers.trained_models.validation_schema import (
    TrainedModelVersionList,
    TrainedModelVersion,
    TrainedModelVersionDatatype,
    PostTrainedModelVersionDatatype,
    PostTrainedModelOut,
)

router = APIRouter(prefix="/trained_models", tags=["Trained Models"])


@router.get(
    "/",
    status_code=200,
    summary="Get all the trained model in the repository",
    name="Get all trained models",
    response_model=TrainedModelVersionList,
)
async def get_all_trained_models():
    response = []
    trained_models = TrainedModel.select().dicts()
    for model in trained_models:
        model_versions = (
            ModelVersion.select()
            .where(ModelVersion.trained_model == model["id"])
            .dicts()
        )
        response.append(TrainedModelVersion(model=model, version=model_versions))
    return TrainedModelVersionList(models=response)


@router.get(
    "/{model_id}",
    status_code=200,
    name="Get a single trained model",
    summary="It returns a trained model given the id",
    responses={404: {"model": str}},
    response_model=TrainedModelVersionDatatype,
)
async def get_trained_model_id(
    model_id: int = Path(
        description="The id of the trained model you want to get", examples=[1]
    ),
):
    try:
        trained_model = TrainedModel.select().where(TrainedModel.id == model_id).dicts()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Model not found"})

    model_versions = (
        ModelVersion.select().where(ModelVersion.trained_model == trained_model).dicts()
    )
    datatypes = (
        TrainModelDatatype.select()
        .where(TrainModelDatatype.trained_model == trained_model)
        .dicts()
    )
    return TrainedModelVersionDatatype(
        model=trained_model.get(), version=model_versions, datatypes=datatypes
    )


@router.post(
    "/",
    name="Create a new training model",
    summary="It creates a trained model given the all the information,version,training infos and feature schema",
    responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}},
)
async def create_model_and_version(payload: PostTrainedModelVersionDatatype):
    """
    This method lets the user create a new training model inside the repository. All the information is ***mandatory***
    and it is validated by the backend. Only datatypes that are already present in the model registry are ***accepted***
    , otherwise a 400 error will be returned. If a new datatype is being used, then it must be inserted with POST manually
    by the user
    """
    try:
        Algorithm.get_by_id(payload.model.algorithm)
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Algorithm not found"})

    datatypes = payload.datatypes
    db_datatypes = []
    for datatype in datatypes:
        datatype, _ = DataType.get_or_create(
            type=datatype.type, is_categorical=datatype.is_categorical
        )
        db_datatypes.append(datatype)

    trained_model, _ = TrainedModel.get_or_create(**payload.model.model_dump())
    model_version = payload.version.model_dump()
    model_version["trained_model"] = trained_model
    model_version = ModelVersion.create(**model_version)
    return PostTrainedModelOut(
        trained_model_id=trained_model.id, model_version_id=model_version.id
    )


@router.delete(
    "/{model_id}",
    status_code=200,
    name="Deletes a trained model",
    summary="Given an id it deletes only a specific version from the trained model leaving the model intact",
    responses={404: {"model": str}},
)
async def delete_train_model(
    model_id: int = Path(
        description="The id of the trained model you want to get", examples=[1]
    ),
    version_name: str = Query(default=None, description="The version to delete"),
):
    """
    This method lets the user delete a specific trained model in the registry, this operation will delete
    all the trained model versions, feature schema and as well as training info. If not present, an 404 error will be raised.
    The query parameter `version_id` (default ***None***) lets the user delete a specific version and associated training info,
    leaving the trained model data and feature schema untouched.
    """
    try:
        trained_model = TrainedModel.get_by_id(model_id)
    except peewee.DoesNotExist:
        return JSONResponse(
            status_code=404, content={"message": "Trained model not found"}
        )

    if version_name is None:
        TrainedModel.delete_by_id(trained_model)
        return JSONResponse(status_code=200, content=trained_model.id)
    else:
        ModelVersion.select().where(
            trained_model == trained_model and version_name == version_name
        ).get().delete_instance()
        return JSONResponse(status_code=200, content=version_name)
