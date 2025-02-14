
from fastapi import APIRouter,Path
from fastapi.params import Query
from starlette.responses import JSONResponse

from ..database.schema import TrainedModel, Features,TrainingInfo,ModelVersion,db,DataType,Algorithm
from ..database.handlers import trained_models as db_handler
from ..database.validation.schema import TrainedModel as PydanticTrainedModel, TrainedModelAndVersionIds, \
    TrainedModelAndVersions, \
    CreateTrainedModel, CreateModelVersion, CreateFeatures, CreateTrainingInfo,TrainedModelAndFeatureSchema

from peewee import DoesNotExist, IntegrityError,fn


router = APIRouter(prefix="/trained_models", tags=['Trained Models'])

@router.get("/",
            status_code=200,
            summary = "Get all the trained model in the repository",
            name = "Get all trained models",
            description="This method returns all the trained models present in the registry, if the query parameter"
                        " include_versions_ids is passed then for each model it is returned a list of all the version ids"
                        " it has",
            response_model=list[PydanticTrainedModel] | list[TrainedModelAndVersionIds])
async def get_all_trained_models(include_version_ids: bool | None = Query(description="Include a list of version ids"
                                " for each trained model",default=False)):
    if not include_version_ids:
        results = [PydanticTrainedModel(**trained_models) for trained_models in
                   TrainedModel.select(TrainedModel,Algorithm.name.alias('algorithm_name')).join(Algorithm).dicts()]
        return results
    else: return db_handler.get_models_and_version_ids()


@router.get("/{trained_model_id}",
            status_code=200,
            name="Get a single trained model",
            summary="It returns a trained model given the id",
            description="Given an id it returns a trained model. If the query parameter include_version is passed, then "
                        "it also returned all the versions that the model has. If include_version is True, it can be re"
                        "trieved a specific version by passing the version id with the query parameter version_id",
            responses={404: {"model": str}},
            response_model=TrainedModelAndFeatureSchema | TrainedModelAndVersions)
async def get_trained_model_id(trained_model_id: int = Path(description="The id of the trained model you want to get",examples=1)
                               ,include_versions: bool | None = Query(description="If the client wants all the versions "
                                                                                  "associated with the trained model",default=False),
                               version_id: int | None = Query(description="If the client wants to retrieve a specific "
                                                                                 "version", default=None)
                               ):
    if version_id or include_versions:
        try:
            return db_handler.get_trained_model_versions(trained_model_id, version_id)
        except DoesNotExist:
            return JSONResponse(status_code=404, content={"message": "Trained Model not found"})
    else:
        try:
            # Fetching the feature schema
            trained_model = (TrainedModel.select(
                TrainedModel,fn.JSON_AGG(
                    fn.JSON_BUILD_OBJECT('feature_name',Features.feature_name,'feature_position',Features.feature_position
                                         ,'is_categorical',DataType.is_categorical,'datatype',DataType.type))
            .alias("feature_schema"),Algorithm.name.alias('algorithm_name'))
                     .join(Algorithm, on=TrainedModel.algorithm_id == Algorithm.id)
                     .switch(TrainedModel)
                     .join(Features)
                     .join(DataType)
                     .where(TrainedModel.id == trained_model_id)
                     .group_by(TrainedModel.id,Algorithm.name)).dicts().get()
        except DoesNotExist:
            return JSONResponse(status_code=404, content={"message": "No trained model has been found with this id"})
        return TrainedModelAndFeatureSchema(**trained_model)



@router.post("/",
            name="Create a new training model",
            summary="It creates a trained model given the all the information,version,training infos and feature schema",
            description="Given a version,training infos, feature schema and information about the model it creates a new"
                        " trained model.",
            responses={500: {"model": str}, 400: {"model":str},201:{"model":str}})
async def create_model_and_version(trained_model: CreateTrainedModel,
                                   version: CreateModelVersion,
                                   training_info: CreateTrainingInfo,
                                   feature_schema: list[CreateFeatures]):
    with db.atomic() as transaction:
         try:
               saved_tr = TrainedModel.create(**trained_model.model_dump())
         except IntegrityError:
             return JSONResponse(status_code=400, content={'message':"No algorithm has been found with this id"})
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
               summary = "Given an id it deletes only a specific version from the trained model leaving the model intact",
               description="This method given an id it deletes all the information of a trained model. If the version_id it"
                           "is passed it only deletes that version leaving the model intact ",
               responses = {404: {"model": str}}
                )
async def delete_train_model(trained_model_id: int,
                             version_id: int | None = Query(description="The id of the version to delete",default=None)):
    try:
        model = TrainedModel.get_by_id(trained_model_id)
    except DoesNotExist:
        return JSONResponse(status_code=404, content={'message': "Model not present"})

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
        # This is the only case we need to return due to the fact that the client is trying to delete a specific version
        # Even if no version is found above, there is no anomalous behaviour. Since the for loop will not be executed
        # and only the model will be deleted
        if len(query.dicts()) == 0:
            return JSONResponse(status_code=404, content={'message': "This version has not been found!"})

    for row in query.dicts():
        ModelVersion.delete().where(ModelVersion.id == row["version_id"]).execute()
        TrainingInfo.delete().where(TrainingInfo.id == row["training_id"]).execute()

    if version_id is None:
        Features.delete().where(Features.trained_model == trained_model_id).execute()
        model.delete_instance()
