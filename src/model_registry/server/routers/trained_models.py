
from fastapi import APIRouter, HTTPException,Path
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.annotation import Annotated
from starlette.responses import JSONResponse
from database.schema import TrainedModel
from database.validation.schema import TrainedModel as PydanticTrainedModel, TrainedModelAndVersionIds, TrainedModelAndVersions,\
    CreateTrainedModel,CreateModelVersion,CreateFeatures,CreateTrainingInfo
from database.validation.schema import ModelVersion as PydanticVersion
from database.handlers import tm_handler as db_handler
from peewee import DoesNotExist, Query

router = APIRouter(prefix="/trained_models")



@router.get("/",
            status_code=200,
            summary = "Get all the trained model in the repository",
            name = "Get all trained models")
async def get_all_trained_models() -> list[PydanticTrainedModel]:
    results = [trained_models for trained_models in TrainedModel.select().dicts()]
    return results

@router.get("/versions",
            status_code=200,
            name = "Get all the trained models' versions",
            summary = "It returns all the version ids of all the trained models",
            )
async def get_trained_models_and_versions()-> list[TrainedModelAndVersionIds]:
    models = db_handler.get_models_and_versions()
    return models

@router.get("/{trained_model_id}",
            status_code=200,
            name="Get a single trained model",
            summary="It returns a trained model given the id",
            responses={404: {"model": str}},
            response_model=PydanticTrainedModel)
async def get_trained_model_id(trained_model_id: int = Path(description="The id of the trained model you want to get",
                                                            example=1)):
    try:
        train_model = db_handler.get_by_id(trained_model_id)
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return train_model

@router.get("/{trained_model_id}/versions", status_code=200,
            name="Get a single trained model and all the versions",
            summary="It returns a trained model given the id and all his versions. If given the version id as query argument"
                    " it will return that specific version",
            responses={404: {"model": str}},
            response_model=TrainedModelAndVersions)
async def get_all_train_model_versions(trained_model_id: int = Path(description="The id of the trained model you want to get",
                                                            example=1),
                                       version_id: int | None = None):
    try:
        return db_handler.get_trained_model_versions(trained_model_id, version_id)
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Trained Model not found"})


@router.post("/", status_code=201,
            name="Create a new training model",
            summary="It creates a trained model given the all the information,version,training infos and feature schema",
            responses={404: {"model": str}})
async def create_model_and_version(trained_model: CreateTrainedModel):
                                   # version: CreateModelVersion,
                                   # training_info: CreateTrainingInfo,
                                   # feature_schema: list[CreateFeatures]):
      pass
#     validated_model = tm_valhandler.validate_model(trained_model)
#     try:
#         db_handler.save_model(validated_model,session,refresh=True)
#     except IntegrityError:
#         raise HTTPException(status_code=400, detail="The value of algorithm_name must be a valid system model. No system model with such value is present")
#
#     try:
#         validated_features = fs_valhandler.validate_all_schemas(feature_schema)
#     except NoResultFound:
#         raise HTTPException(status_code=400, detail="This kind of datatype is not supported. Please add it to use it")
#
#     for feature in validated_features:
#         feature.trained_model_id = validated_model.id
#     db_feature_handler.save_all_features(validated_features,session)
#
#     validated_training_info = tr_info_valhandler.validate_model(training_info)
#     db_info_handler.save_model(validated_training_info,session,refresh=True)
#
#     validated_version = mv_valhandler.validate_model(version)
#     validated_version.training_info_id = validated_training_info.id
#     validated_version.trained_model_id = validated_model.id
#
#     db_model_version_handler.save_model(validated_version,session)
#
#     return {"message": "Successfully saved model with the following id", "id": validated_model.id}
#
# @router.delete("/{trained_model_id}", status_code=200)
# async def delete_train_model(trained_model_id: int, session: SessionDep):
#     try:
#         train_model = db_handler.get_by_id(trained_model_id)
#     except NoResultFound:
#         raise HTTPException(status_code=404, detail="No trained instance with id: " + str(trained_model_id) + " has been found")
#     db_handler.delete_trained_model_schemas(train_model, session)
#     try:
#         _, versions_infos = db_handler.get_trained_model_versions(model_id=trained_model_id, session=session, version_id=None)
#     except NoModelFound as e:
#         raise HTTPException(status_code=404, detail=f"{e}")
#     except NoVersions:
#         pass
#     else:
#         for elem in versions_infos:
#             session.delete(elem["version_info"])
#             session.delete(elem["training_info"])
#         session.commit()
#
#     session.delete(train_model)
#     session.commit()
#
# @router.delete("/{trained_model_id}/versions", status_code=200)
# async def delete_train_model_version(trained_model_id: int,session: SessionDep, version_id: int | None = None):
#     try:
#         _, version_info = db_handler.get_trained_model_versions(trained_model_id, version_id, session)
#     except (NoModelFound,NoVersions,VersionNotFound) as e:
#         raise HTTPException(status_code=404, detail=f"{e}")
#
#     for elem in version_info:
#         session.delete(elem["version_info"])
#         session.delete(elem["training_info"])
#     session.commit()