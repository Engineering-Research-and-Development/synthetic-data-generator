
from fastapi import APIRouter,Path
from starlette.responses import JSONResponse

from database.schema import TrainedModel, Features,TrainingInfo,ModelVersion,db,DataType
from database.handlers import trained_models as db_handler
from database.validation.schema import TrainedModel as PydanticTrainedModel, TrainedModelAndVersionIds, \
    TrainedModelAndVersions, \
    CreateTrainedModel, CreateModelVersion, CreateFeatures, CreateTrainingInfo,TrainedModelAndFeatureSchema

from peewee import DoesNotExist, IntegrityError,fn


router = APIRouter(prefix="/trained_models")

@router.get("/",
            status_code=200,
            summary = "Get all the trained model in the repository",
            name = "Get all trained models")
async def get_all_trained_models() -> list[PydanticTrainedModel]:
    results = [PydanticTrainedModel(**trained_models) for trained_models in TrainedModel.select().dicts()]
    return results

@router.get("/versions",
            status_code=200,
            name = "Get all the trained models' versions",
            summary = "It returns all the version ids of all the trained models",
            )
async def get_trained_models_and_versions()-> list[TrainedModelAndVersionIds]:
    models = db_handler.get_models_and_version_ids()
    return models

@router.get("/{trained_model_id}",
            status_code=200,
            name="Get a single trained model",
            summary="It returns a trained model given the id",
            responses={404: {"model": str}},
            response_model=TrainedModelAndFeatureSchema)
async def get_trained_model_id(trained_model_id: int = Path(description="The id of the trained model you want to get",                                                        example=1)):
    try:
        # Fetching the feature schema
        trained_model = (TrainedModel.select(
            TrainedModel,fn.JSON_AGG(
                fn.JSON_BUILD_OBJECT('feature_name',Features.feature_name,'feature_position',Features.feature_position
                                     ,'is_categorical',DataType.is_categorical,'datatype',DataType.type))
        .alias("feature_schema"))
                 .join(Features)
                 .join(DataType)
                 .where(TrainedModel.id == trained_model_id)
                 .group_by(TrainedModel.id)).dicts().get()
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return TrainedModelAndFeatureSchema(**trained_model)



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


@router.post("/",
            name="Create a new training model",
            summary="It creates a trained model given the all the information,version,training infos and feature schema",
            responses={500: {"model": str}, 400: {"model":str},201:{"model":str}})
async def create_model_and_version(trained_model: CreateTrainedModel,
                                   version: CreateModelVersion,
                                   training_info: CreateTrainingInfo,
                                   feature_schema: list[CreateFeatures]):
    with db.atomic() as transaction:
         try:
               saved_tr = TrainedModel.create(**trained_model.model_dump())
         except IntegrityError:
             return JSONResponse(status_code=500, content={'message':"Error in processing the request"})
         # We need to check if the datatypes passed are allowed, i.e. present in the registry
         for feature in feature_schema:
             try:
                datatype =  DataType.select().where(DataType.type == feature.datatype)\
                .where(DataType.is_categorical == feature.is_categorical).get()
             except DoesNotExist:
                 transaction.rollback()
                 return JSONResponse(status_code=400, content={'message': "The datatype is currently not supported"
                                                                          ", to use it add it with POST /datatype"})
             try:
                 Features.insert(feature_name=feature.feature_name,feature_position=feature.feature_position
                                 ,datatype=datatype.id,trained_model=saved_tr.id).execute()
             except IntegrityError:
                 transaction.rollback()
                 return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

         try:
             save_training_info = TrainingInfo.create(**training_info.model_dump())
         except IntegrityError:
             transaction.rollback()
             return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

         try:
             ModelVersion.insert(**version.model_dump(),training_info = save_training_info.id
                                                     ,trained_model = saved_tr.id).execute()
         except IntegrityError:
             transaction.rollback()
             return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

    return JSONResponse(status_code=201,content={"message": "Successfully saved model with the following id", "id": saved_tr.id})


@router.delete("/{trained_model_id}",
               status_code=200,
               name = "Deletes a trained model",
               summary = "Given an id it deletes a trained model with his feature schemas,versions and training info from the registry",
               responses = {404: {"model": str}}
                )
async def delete_train_model(trained_model_id: int):
    try:
        model = TrainedModel.get_by_id(trained_model_id)
    except DoesNotExist:
        return JSONResponse(status_code=404, content={'message': "Model not present"})
    Features.delete().where(Features.trained_model == trained_model_id).execute()
    query = (
        ModelVersion.select(ModelVersion.id.alias("version_id"),
                            TrainingInfo.id.alias("training_id"))
            .join(TrainingInfo).where(ModelVersion.trained_model == trained_model_id)
    )
    for row in query.dicts():
        ModelVersion.delete().where(ModelVersion.id == row["version_id"]).execute()
        TrainingInfo.delete().where(TrainingInfo.id == row["training_id"]).execute()
    model.delete_instance()

@router.delete("/{trained_model_id}/versions",
               status_code=200,
               name = "Deletes all versions & training info of a trained model",
               summary = "Given an id it deletes all versions and training info of a trained model, if the query param version_id"
                         " is passed it deletes only that version id",
               responses = {404: {"model": str}}
                )
async def delete_train_model_version(trained_model_id: int, version_id: int | None = None):
    if version_id is None:
        query = (
            ModelVersion.select(ModelVersion.id.alias("version_id"),
                                TrainingInfo.id.alias("training_id"))
                .join(TrainingInfo).where(ModelVersion.trained_model == trained_model_id)
        )
    else:
        query = (
            ModelVersion.select(ModelVersion.id.alias("version_id"),
                                TrainingInfo.id.alias("training_id"))
            .join(TrainingInfo)
            .where(ModelVersion.trained_model == trained_model_id)
            .where(ModelVersion.id == version_id)
        )
    if len(query.dicts()) == 0:
        return JSONResponse(status_code=404, content={'message': "Either this model is not present or it "
                                                                 "has no versions!"})
    for row in query.dicts():
        ModelVersion.delete().where(ModelVersion.id == row["version_id"]).execute()
        TrainingInfo.delete().where(TrainingInfo.id == row["training_id"]).execute()