
from database.schema import TrainedModel, TrainingInfo, ModelVersion,Features,DataType
from database.validation.schema import TrainedModelAndVersionIds\
    ,TrainedModelAndVersions as PydanticTrainedModelAndVersions,ModelVersionAndTrainInfo,ModelVersion as PydanticModelVersion, TrainingInfo as PydanticTrainingInfo
from peewee import fn,JOIN

def get_trained_model_versions(model_id,version_id) -> PydanticTrainedModelAndVersions:
#     query = (TrainedModel.select(
#         # This is done so that .dicts will not overwrite the ids of versions and training info
#         TrainedModel, ModelVersion.id.alias("version_id"),ModelVersion
#         ,TrainingInfo.id.alias("training_id"),TrainingInfo
#         )
#              .join(ModelVersion,JOIN.LEFT_OUTER)
#              .join(TrainingInfo,JOIN.LEFT_OUTER)
#              .where(TrainedModel.id == model_id)
#     )
    # This hack is done so that the attributes inside the validation class can change
    # The above outer join although is more efficient has hardcoded values inside it, so this is more flexible
    if version_id is None:
        query = ModelVersion.select().where(ModelVersion.trained_model_id == model_id)
    else: query = ModelVersion.select().where(ModelVersion.trained_model_id == model_id).where(ModelVersion.id == version_id)
    versions = [PydanticModelVersion(**row) for row in query.dicts()]
    query = TrainingInfo.select(TrainingInfo).join(ModelVersion).where(ModelVersion.trained_model_id == model_id)
    training_infos = [PydanticTrainingInfo(**row) for row in query.dicts()]
    train_and_versions = [ModelVersionAndTrainInfo(version=elem[0],training_info=elem[1]) for elem in zip(versions,training_infos)]
    #Now we get the features
    train_and_features = (TrainedModel.select(
        TrainedModel, fn.JSON_AGG(
            fn.JSON_BUILD_OBJECT('feature_name', Features.feature_name, 'feature_position', Features.feature_position
                                 , 'is_categorical', DataType.is_categorical, 'datatype', DataType.type))
        .alias("feature_schema"))
             .join(Features)
             .join(DataType)
             .where(TrainedModel.id == model_id)
             .group_by(TrainedModel.id)).dicts().get()
    return PydanticTrainedModelAndVersions(**train_and_features,versions=train_and_versions)


def get_models_and_version_ids() -> list[TrainedModelAndVersionIds]:
    query = (TrainedModel.select(
        TrainedModel,fn.STRING_AGG(ModelVersion.id.cast('TEXT'),', ').alias('version_ids'))
             .join(ModelVersion,JOIN.LEFT_OUTER)
             .group_by(TrainedModel.id))
    payload = [TrainedModelAndVersionIds(**row) for row in query.dicts()]
    return payload

