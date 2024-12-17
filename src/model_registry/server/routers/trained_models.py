from fastapi import APIRouter, HTTPException
from model_registry.database.schema import TrainedModel, ModelVersion, FeatureSchema, TrainingInfo
from ...database import model
import sqlalchemy
from ..validation import CreateTrainedModel, CreateModelVersion, CreateTrainingInfo, CreateFeatureSchema, \
    BaseFeatureSchema
from .. import service

router = APIRouter()


# Add a new model to the repository
@router.get("/trained_models",status_code=201)
async def get_all_trained_models():
    return model.select_all(TrainedModel)

# This function is usually called by the generator who wants to know for a given trained model all the version
# and information about them
@router.get("/trained_models/{trained_model_id}",status_code=200)
async def get_trained_model_id(trained_model_id: int):
    return model.select_data_by_id(TrainedModel,trained_model_id)


@router.get("/trained_models/{trained_model_id}/versions",status_code=200)
async def get_all_train_model_versions(trained_model_id: int,version_id: int | None = None):
    model_info,version_and_train = service.get_trained_model_versions(trained_model_id,version_id)
    # Now we get the schema of how the features are disposed in input as well as their data type
    feature_schema = service.get_trained_model_feature_schema(trained_model_id)
    payload = {"model": model_info, "versions":version_and_train,"feature_schema":feature_schema}
    return payload


@router.post("/trained_models",status_code=201)
async def create_model_and_version(trained_model:CreateTrainedModel,feature_schema: list[CreateFeatureSchema],
                                   version: CreateModelVersion | None = None,training_info: CreateTrainingInfo | None = None):
    """
    This function creates a new trained model and if a version and training info are passed they create them as well
    :param trained_model: A new trained model to save
    :param feature_schema: How the features have been ordered in this model version
    :param version: Optional. A version for the trained model passed
    :param training_info: Optional. The training info of a given version
    :return:
    """
    # Validate & save trained model and schema
    validated_model = TrainedModel.model_validate(trained_model)
    model.save_data(validated_model,refresh_data=True)
    validated_features = service.validate_all_schemas(feature_schema)
    # We add the validated schema to the new model created
    # The id of the model is known since it has been refreshed in the session
    for feature in validated_features:
        feature.trained_model_id = validated_model.id
    # Now we can save the feature schema, successfully assigning it to the model
    model.save_all(validated_features)
    # Checking if user has passed only version or training info ( ^ is the pythonic way of defining a xor)
    if (version is None) ^ (training_info is None):
        raise HTTPException(status_code=400,detail="Can NOT insert version or training individually. Both must be passed ")
    # In case both are not None, then we add them
    elif version and training_info:
        # Creating training info
        validated_training_info = TrainingInfo.model_validate(training_info)
        # we need the id to set it to the version
        model.save_data(validated_training_info,refresh_data=True)
        # Creating version
        validated_version = ModelVersion.model_validate(version)
        # Adding the refs
        validated_version.trained_model_id = validated_model.id
        validated_version.training_info_id = validated_training_info.id
        # Saving it
        model.save_data(validated_version)








@router.delete("/trained_models/{trained_model_id}",status_code=200)
async def delete_train_model(system_model_id: int):
    model.delete_data(TrainedModel,system_model_id)


