
from database.schema import TrainedModel, TrainingInfo, ModelVersion
from database.validation.schema import TrainedModelAndVersionIds\
    ,TrainedModelAndVersions as PydanticTrainedModelAndVersions,ModelVersionAndTrainInfo,ModelVersion as PydanticModelVersion, TrainingInfo as PydanticTrainingInfo
from peewee import fn,JOIN

def get_trained_model_versions(model_id) -> PydanticTrainedModelAndVersions:
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
    query = ModelVersion.select().where(ModelVersion.trained_model_id == model_id)
    versions = [PydanticModelVersion(**row) for row in query.dicts()]
    query = TrainingInfo.select(TrainingInfo).join(ModelVersion).where(ModelVersion.trained_model_id == model_id)
    training_infos = [PydanticTrainingInfo(**row) for row in query.dicts()]
    train_and_versions = [ModelVersionAndTrainInfo(version=elem[0],training_info=elem[1]) for elem in zip(versions,training_infos)]
    trained_model = TrainedModel.select().where(TrainedModel.id == model_id).dicts()[0]
    return PydanticTrainedModelAndVersions(**trained_model,versions=train_and_versions)


def get_models_and_version_ids() -> list[TrainedModelAndVersionIds]:
    query = (TrainedModel.select(
        TrainedModel,fn.STRING_AGG(ModelVersion.id.cast('TEXT'),', ').alias('version_ids'))
             .join(ModelVersion,JOIN.LEFT_OUTER)
             .group_by(TrainedModel.id))
    payload = [TrainedModelAndVersionIds(**row) for row in query.dicts()]
    return payload

