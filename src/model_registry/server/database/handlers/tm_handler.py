
from database.schema import TrainedModel, TrainingInfo, ModelVersion, DataType
from database.validation.schema import TrainedModelAndVersionIds,TrainedModel as PydanticTrainedModel\
    ,TrainedModelAndVersions as PydanticTrainedModelAndVersions,ModelVersionAndTrainInfo,ModelVersion as PydanticModelVersion, TrainingInfo as PydanticTrainingInfo
from errors import NoVersions, NoModelFound, VersionNotFound
from peewee import *

def get_trained_model_versions(model_id, version_id) -> PydanticTrainedModelAndVersions:
#     query = (TrainedModel.select(
#         # This is done so that .dicts will not overwrite the ids of versions and training info
#         TrainedModel, ModelVersion.id.alias("version_id"),ModelVersion
#         ,TrainingInfo.id.alias("training_id"),TrainingInfo
#         )
#              .join(ModelVersion,JOIN.LEFT_OUTER)
#              .join(TrainingInfo,JOIN.LEFT_OUTER)
#              .where(TrainedModel.id == model_id)
#     )
    # This stinky code is done so that the attributes inside the validation class can change
    # The above outer join although is more efficient has hardcoded values inside it, so this is more flexible
    query = ModelVersion.select().where(ModelVersion.trained_model_id == model_id)
    versions = [PydanticModelVersion(**row) for row in query.dicts()]
    query = TrainingInfo.select(TrainingInfo).join(ModelVersion).where(ModelVersion.trained_model_id == model_id)
    training_infos = [PydanticTrainingInfo(**row) for row in query.dicts()]
    train_and_versions = [ModelVersionAndTrainInfo(version=elem[0],training_info=elem[1]) for elem in zip(versions,training_infos)]
    trained_model = TrainedModel.select().where(TrainedModel.id == model_id).dicts()[0]
    return PydanticTrainedModelAndVersions(**trained_model,versions=train_and_versions)





    # statement = select(TrainedModel,ModelVersion,TrainingInfo).outerjoin(ModelVersion,onclause=ModelVersion.trained_model_id == TrainedModel.id)\
    #     .outerjoin(TrainingInfo).where(TrainedModel.id == model_id)
    # results = session.exec(statement).all()
    # if len(results) == 0:
    #     raise NoModelFound("No model has been found with this id!")
    # if not results[0][1] :
    #     raise NoVersions("This trained model exists but has no versions!")
    # versions_and_info = []
    # model_info = results[0][0]
    # flag = False
    # for elem in results:
    #     versions_and_info.append({"version_info":elem[1],"training_info":elem[2]})
    #     if version_id and elem[1].id == version_id:
    #         return model_info,[{"version_info":elem[1],"training_info":elem[2]}]
    # if version_id and not flag:
    #     raise VersionNotFound("The model exists but it has not a version with id:" + str(version_id))
    # # Returning model information and version paired with training information
    # return model_info,versions_and_info

#
# def get_trained_model_feature_schema(trained_model_id: int, session: SessionDep) -> list[dict[str,SQLModel]]:
#     # The feature schema primary key is based as a ternary (trained_model_id,data_type_id,feature_pos)
#     # So for a given trained model, we just query the Feature Schema table for the trained_model_id
#     # A further join is done so that we get also the name of the feature
#     statement = select(FeatureSchema, DataType).join(DataType).where(FeatureSchema.trained_model_id == trained_model_id)
#     results = session.exec(statement).all()
#     # Building payload as docs dictate
#     data_list = []
#     for feature,data_type in results:
#         data_list.append({"column_name":feature.feature_name,"categorical":data_type.is_categorical,
#                           "column_datatype":data_type.type,"column_position":feature.feature_position})
#     return data_list
#
# def delete_trained_model_schemas(trained_model: TrainedModel, session: SessionDep):
#
#     statement = select(FeatureSchema).where(FeatureSchema.trained_model_id == trained_model.id)
#     results = session.exec(statement).all()
#     for result in results:
#         session.delete(result)
#     session.commit()
#
#
# def delete_trained_model_version(trained_model: TrainedModel,version_id: int, session: SessionDep):
#     if version_id is None:
#         statement = select(ModelVersion,TrainingInfo).join(TrainingInfo).where(ModelVersion.trained_model_id == trained_model.id)
#     else:
#         statement = select(ModelVersion,TrainingInfo).join(TrainingInfo).where(ModelVersion.trained_model_id == trained_model.id)\
#             .where(ModelVersion.id == version_id)
#     results = session.exec(statement).all()
#     return results

def get_models_and_versions() -> list[TrainedModelAndVersionIds]:
    query = (TrainedModel.select(
        TrainedModel,fn.STRING_AGG(ModelVersion.id.cast('TEXT'),', ').alias('version_ids'))
             .join(ModelVersion,JOIN.LEFT_OUTER)
             .group_by(TrainedModel.id))
    payload = [TrainedModelAndVersionIds(**row) for row in query.dicts()]
    return payload
# def get_all(session: SessionDep) -> list[TrainedModel]:
#     statement = select(TrainedModel)
#     results = session.exec(statement)
#     return results.all()
#
def get_by_id(train_id: int) -> PydanticTrainedModel:
    query = TrainedModel.select().where(TrainedModel.id == train_id)
    return [PydanticTrainedModel(**row) for row in query.dicts()][0]

# def save_model(model: TrainedModel,session: SessionDep, refresh: bool = False) -> None:
#     session.add(model)
#     session.commit()
#     if refresh:
#         session.refresh(model)

