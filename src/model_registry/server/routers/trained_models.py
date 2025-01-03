from fastapi import APIRouter, HTTPException
from model_registry.database.schema import TrainedModel, ModelVersion, TrainingInfo
from model_registry.database import model
from sqlalchemy.exc import IntegrityError, NoResultFound
from model_registry.server.validation import CreateTrainedModel, CreateModelVersion, CreateTrainingInfo, CreateFeatureSchema
from model_registry.server.service import tm_service as service

# Needed for FASTApi
router = APIRouter()


# Add a new model to the repository
@router.get("/trained_models",status_code=200)
async def get_all_trained_models():
    """
    This function return all the trained models present in the model registry
    :return:
    """
    return model.select_all(TrainedModel)

# This function is usually called by the generator who wants to know for a given trained model all the version
# and information about them
@router.get("/trained_models/{trained_model_id}",status_code=200)
async def get_trained_model_id(trained_model_id: int):
    """
    This function given a train model id it returns it
    :param trained_model_id: Integer. A train model id
    :return: A trained model
    """
    try:
        train_model = model.select_data_by_id(TrainedModel,trained_model_id)
    except NoResultFound:
        raise HTTPException(status_code=404,detail="No trained instance with id: " + str(trained_model_id) + " has been found")
    return train_model


@router.get("/trained_models/{trained_model_id}/versions",status_code=200)
async def get_all_train_model_versions(trained_model_id: int,version_id: int | None = None):
    """
    This function given a trained model id it returns all the versions associated with it as well as the feature schema.
    Optionally a specific version id can be passed so that only that version will be returned
    :param trained_model_id: Integer. The version of the trained model
    :param version_id: Optional. Integer. The id of the version
    :return: A trained model with the associated versions
    """
    model_info,version_and_train = service.get_trained_model_versions(trained_model_id,version_id)
    # Now we get the schema of how the features are disposed in input as well as their data type
    feature_schema = service.get_trained_model_feature_schema(trained_model_id)
    payload = {"model": model_info, "versions":version_and_train,"feature_schema":feature_schema}
    return payload


@router.post("/trained_models",status_code=201)
async def create_model_and_version(trained_model:CreateTrainedModel,version: CreateModelVersion,
                                   training_info: CreateTrainingInfo,training_data_info: list[CreateFeatureSchema]):
    """
    This function creates a new trained model and if a version and training info are passed they create them as well
    :param trained_model: A new trained model to save
    :param version:  A version for the trained model passed
    :param training_info: The training info of a given version
    :param training_data_info: How the features have been ordered in this model version
    :return:
    """

    validated_model = TrainedModel.model_validate(trained_model)
    try:
        model.save_data(validated_model,refresh_data=True)
    except IntegrityError:
        raise HTTPException(status_code=400,detail="The value of algorithm_name must be a valid system model. No system model"
                                                   " with such value is present")
    validated_features = service.validate_all_schemas(training_data_info)
    # We add the validated schema to the new model created
    # The id of the model is known since it has been refreshed in the session
    for feature in validated_features:
        feature.trained_model_id = validated_model.id
    model.save_all(validated_features)
    validated_training_info = TrainingInfo.model_validate(training_info)
    model.save_data(validated_training_info,refresh_data=True)
    validated_version = ModelVersion.model_validate(version)
    validated_version.training_info_id = validated_training_info.id
    validated_version.trained_model_id = validated_model.id
    model.save_data(validated_version)
    return {"message":"Successfully saved model with the following id","id": validated_model.id}



@router.delete("/trained_models/{trained_model_id}",status_code=200)
async def delete_train_model(trained_model_id: int):
    """
    Given an id, it deletes the train model and all associated versions, training infos and feature schemas
    :param trained_model_id: Integer. The id of the trained model to delete
    :return:
    """
    try:
        train_model = model.select_data_by_id(TrainedModel,trained_model_id)
    except NoResultFound:
        raise HTTPException(status_code=404,detail="No trained instance with id: " + str(trained_model_id) + " has been found")
    service.delete_trained_model_schemas(train_model)
    # Now we get all versions and training info and delete them
    _,versions_infos = service.get_trained_model_versions(trained_model_id)
    for elem in versions_infos:
        model.delete_instance(elem["version_info"])
        model.delete_instance(elem["training_info"])
    model.delete_instance(train_model)


@router.delete("/trained_models/{trained_model_id}/versions/",status_code=200)
async def delete_train_model_version(trained_model_id: int,version_id: int | None = None):
    """
    This function given a trained model id deletes the passed version id. Otherwise, it deletes all versions associated
    with the trained model
    :param trained_model_id: The id of the trained model to delete from
    :param version_id: Optional. The id of the particular version that wants to be deleted
    :return:
    """
    _,version_info = service.get_trained_model_versions(trained_model_id,version_id)
    for elem in version_info:
        model.delete_instance(elem["version_info"])
        model.delete_instance(elem["training_info"])


