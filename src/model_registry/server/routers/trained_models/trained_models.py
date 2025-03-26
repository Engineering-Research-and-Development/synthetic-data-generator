from fastapi import APIRouter, Path
from peewee import DoesNotExist, IntegrityError, fn
from starlette.responses import JSONResponse

from database.handlers import trained_models as db_handler
from database.schema import (
    TrainedModel,
    TrainModelDatatype,
    TrainingInfo,
    ModelVersion,
    db,
    DataType,
    Algorithm,
)
from database.validation.schema import (
    TrainedModel as PydanticTrainedModel,
    TrainedModelAndVersionIds,
    TrainedModelAndVersions,
    TrainedModel,
    CreateModelVersion,
    CreateFeatures,
    TrainingInfo,
    TrainedModelAndFeatureSchema,
)

router = APIRouter(prefix="/trained_models", tags=["Trained Models"])


@router.get(
    "/",
    status_code=200,
    summary="Get all the trained model in the repository",
    name="Get all trained models",
    response_model=list[PydanticTrainedModel]
    | list[TrainedModelAndVersionIds]
    | dict[int, PydanticTrainedModel]
    | dict[int, TrainedModelAndVersionIds],
)
async def get_all_trained_models(
    include_version_ids: bool = False,
    index_by_id: bool = False,
):
    """
    This method returns all the trained models present in the registry, if the query parameter
    `include_versions_ids` = ***True*** then for each model it is returned a list having all the ids of the versions
    that it has. The query parameter `index_by_id` (default ***False***) if set to ***True*** will return all the
    trained models in registry as a dictionary keyed by each trained model key.
    """
    if not include_version_ids:
        if not index_by_id:
            results = [
                PydanticTrainedModel(**trained_models)
                for trained_models in TrainedModel.select(
                    TrainedModel, Algorithm.name.alias("algorithm_name")
                )
                .join(Algorithm)
                .dicts()
            ]
        else:
            results = {
                trained_models["id"]: PydanticTrainedModel(**trained_models)
                for trained_models in TrainedModel.select(
                    TrainedModel, Algorithm.name.alias("algorithm_name")
                )
                .join(Algorithm)
                .dicts()
            }
        return results

    else:
        return db_handler.get_models_and_version_ids(index_by_id)


@router.get(
    "/{trained_model_id}",
    status_code=200,
    name="Get a single trained model",
    summary="It returns a trained model given the id",
    responses={404: {"model": str}},
    response_model=TrainedModelAndFeatureSchema | TrainedModelAndVersions,
)
async def get_trained_model_id(
    trained_model_id: int = Path(
        description="The id of the trained model you want to get", examples=[1]
    ),
    include_versions: bool = False,
    version_id: int = None,
    include_training_info: bool = False,
):
    """
    Given an id, it returns a trained model. This method accepts the following query parameters:

    - `include_version` (default: ***False***)
      If passed, all the versions associated with the model are returned.

    - `version_id` (default: ***None***)
      If passed, a specific version with the given ID is returned. It ***overrides*** `include_version` if provided.

    - `include_training_info` (default: ***False***)
      If passed, it returns all the corresponding training information for each version.


    """
    if version_id or include_versions:
        try:
            return db_handler.get_trained_model_versions(
                trained_model_id, version_id, include_training_info
            )
        except DoesNotExist:
            return JSONResponse(
                status_code=404, content={"message": "Trained Model not found"}
            )
    else:
        try:
            # Fetching the feature schema
            trained_model = (
                (
                    TrainedModel.select(
                        TrainedModel,
                        fn.JSON_AGG(
                            fn.JSON_BUILD_OBJECT(
                                "feature_name",
                                TrainModelDatatype.feature_name,
                                "feature_position",
                                TrainModelDatatype.feature_position,
                                "is_categorical",
                                DataType.is_categorical,
                                "datatype",
                                DataType.type,
                            )
                        ).alias("feature_schema"),
                        Algorithm.name.alias("algorithm_name"),
                    )
                    .join(Algorithm, on=TrainedModel.algorithm_id == Algorithm.id)
                    .switch(TrainedModel)
                    .join(TrainModelDatatype)
                    .join(DataType)
                    .where(TrainedModel.id == trained_model_id)
                    .group_by(TrainedModel.id, Algorithm.name)
                )
                .dicts()
                .get()
            )
        except DoesNotExist:
            return JSONResponse(
                status_code=404,
                content={"message": "No trained model has been found with this id"},
            )
        return TrainedModelAndFeatureSchema(**trained_model)


@router.get(
    "/image-paths/",
    status_code=200,
    name="Get a single trained model by their image id, which is the name of the folder given by the generator",
    summary="It returns a trained model given the passed image id",
    responses={404: {"model": str}},
    response_model=dict[str, TrainedModel],
)
async def get_all_trained_model_by_image_path():
    """
    This function returns all the trained models present in the repo indexed by their version's image path
    """
    try:
        results = (
            TrainedModel.select(TrainedModel, ModelVersion.image_path)
            .join(ModelVersion)
            .dicts()
        )
    except DoesNotExist:
        return JSONResponse(
            status_code=404, content={"message": "Trained Model not found"}
        )
    payload = {}
    for elem in results:
        path = elem["image_path"]
        del elem["image_path"]
        payload[path] = TrainedModel(**elem)
    return payload


@router.get(
    "/image-paths/{image_id}",
    status_code=200,
    name="Get a single trained model by their image id, which is the name of the folder given by the generator",
    summary="It returns a trained model given the passed image id",
    responses={404: {"model": str}},
    response_model=TrainedModel,
)
async def get_trained_model_by_image_path(
    image_id: str = Path(
        description="The id of the trained model you want to get", examples=[1]
    ),
):
    """
    Given an image id, which is the name of the folder given by the generator, it returns a trained model.
    """
    try:
        tr = (
            TrainedModel.select(TrainedModel)
            .join(ModelVersion)
            .where(ModelVersion.image_path == image_id)
            .dicts()
            .get()
        )
    except DoesNotExist:
        return JSONResponse(
            status_code=404, content={"message": "Trained Model not found"}
        )
    return TrainedModel(**tr)


@router.post(
    "/",
    name="Create a new training model",
    summary="It creates a trained model given the all the information,version,training infos and feature schema",
    responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}},
)
async def create_model_and_version(
    trained_model: TrainedModel,
    version: CreateModelVersion,
    training_info: TrainingInfo,
    feature_schema: list[CreateFeatures],
):
    """
    This method lets the user create a new training model inside the repository. All the information is ***mandatory***
    and it is validated by the backend. Only datatypes that are already present in the model registry are ***accepted***
    , otherwise a 400 error will be returned. If a new datatype is being used, then it must be inserted with POST manually
    by the user
    """
    with db.atomic() as transaction:
        saved_tr, created = TrainedModel.get_or_create(**trained_model.model_dump())
        # We need to check if the datatypes passed are allowed, i.e. present in the registry
        for feature in feature_schema:
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
                TrainModelDatatype.insert(
                    feature_name=feature.feature_name,
                    feature_position=feature.feature_position,
                    datatype=datatype.id,
                    trained_model=saved_tr.id,
                ).execute()
            except IntegrityError:
                transaction.rollback()
                return JSONResponse(
                    status_code=500,
                    content={"message": "Error in processing the request"},
                )

        try:
            saved_model_version = ModelVersion.create(
                **version.model_dump(), trained_model=saved_tr.id
            )
        except IntegrityError:
            transaction.rollback()
            return JSONResponse(
                status_code=500, content={"message": "Error in processing the request"}
            )

        try:
            TrainingInfo.insert(
                **training_info.model_dump(), model_version_id=saved_model_version.id
            ).execute()
        except IntegrityError:
            transaction.rollback()
            return JSONResponse(
                status_code=500, content={"message": "Error in processing the request"}
            )

    return JSONResponse(
        status_code=201,
        content={
            "message": "Successfully saved model with the following id",
            "id": saved_tr.id,
        },
    )


@router.delete(
    "/{trained_model_id}",
    status_code=200,
    name="Deletes a trained model",
    summary="Given an id it deletes only a specific version from the trained model leaving the model intact",
    responses={404: {"model": str}},
)
async def delete_train_model(
    trained_model_id: int,
    version_id: int = None,
):
    """
    This method lets the user delete a specific trained model in the registry, this operation will delete
    all the trained model versions, feature schema and as well as training info. If not present, an 404 error will be raised.
    The query parameter `version_id` (default ***None***) lets the user delete a specific version and associated training info,
    leaving the trained model data and feature schema untouched.
    """
    if version_id:
        try:
            version = ModelVersion.get_by_id(version_id)
        except DoesNotExist:
            return JSONResponse(
                status_code=404, content={"message": "Model not present"}
            )
        version.delete_instance()
    else:
        try:
            model = TrainedModel.get_by_id(trained_model_id)
        except DoesNotExist:
            return JSONResponse(
                status_code=404, content={"message": "Model not present"}
            )
        model.delete_instance()
