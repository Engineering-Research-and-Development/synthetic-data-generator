from fastapi import APIRouter, Path

from database.schema import TrainedModel, ModelVersion
from routers.trained_models.validation_schema import (
    TrainedModelVersionList,
    TrainedModelVersion,
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
    """
    This method returns all the trained models present in the registry, if the query parameter
    `include_versions_ids` = ***True*** then for each model it is returned a list having all the ids of the versions
    that it has. The query parameter `index_by_id` (default ***False***) if set to ***True*** will return all the
    trained models in registry as a dictionary keyed by each trained model key.
    """
    response = []
    trained_models = TrainedModel.select().dicts()
    for model in trained_models:
        model_versions = (
            ModelVersion.select()
            .where(ModelVersion.trained_model == model["id"])
            .dicts()
        )
        response.append(TrainedModelVersion(model=model, version=model_versions))
    response = TrainedModelVersionList(models=response)
    return response


@router.get(
    "/{model_id}",
    status_code=200,
    name="Get a single trained model",
    summary="It returns a trained model given the id",
    responses={404: {"model": str}},
)
async def get_trained_model_id(
    model_id: int = Path(
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
    pass


@router.post(
    "/",
    name="Create a new training model",
    summary="It creates a trained model given the all the information,version,training infos and feature schema",
    responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}},
)
async def create_model_and_version():
    """
    This method lets the user create a new training model inside the repository. All the information is ***mandatory***
    and it is validated by the backend. Only datatypes that are already present in the model registry are ***accepted***
    , otherwise a 400 error will be returned. If a new datatype is being used, then it must be inserted with POST manually
    by the user
    """
    pass


@router.delete(
    "/{model_id}}",
    status_code=200,
    name="Deletes a trained model",
    summary="Given an id it deletes only a specific version from the trained model leaving the model intact",
    responses={404: {"model": str}},
)
async def delete_train_model(
    version_id: int = None,
):
    """
    This method lets the user delete a specific trained model in the registry, this operation will delete
    all the trained model versions, feature schema and as well as training info. If not present, an 404 error will be raised.
    The query parameter `version_id` (default ***None***) lets the user delete a specific version and associated training info,
    leaving the trained model data and feature schema untouched.
    """
    pass
