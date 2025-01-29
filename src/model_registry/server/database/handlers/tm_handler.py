
from model_registry.database.schema import TrainedModel, TrainingInfo, ModelVersion, FeatureSchema, DataType
from model_registry.server.errors import NoVersions, NoModelFound, VersionNotFound
from model_registry.server.dependencies import SessionDep
from sqlmodel import select, SQLModel

def get_trained_model_versions(model_id, version_id, session: SessionDep) -> tuple:
    statement = select(TrainedModel,ModelVersion,TrainingInfo).outerjoin(ModelVersion,onclause=ModelVersion.trained_model_id == TrainedModel.id)\
        .outerjoin(TrainingInfo).where(TrainedModel.id == model_id)
    results = session.exec(statement).all()
    if len(results) == 0:
        raise NoModelFound("No model has been found with this id!")
    if not results[0][1] :
        raise NoVersions("This trained model exists but has no versions!")
    versions_and_info = []
    model_info = results[0][0]
    flag = False
    for elem in results:
        versions_and_info.append({"version_info":elem[1],"training_info":elem[2]})
        if version_id and elem[1].id == version_id:
            return model_info,[{"version_info":elem[1],"training_info":elem[2]}]
    if version_id and not flag:
        raise VersionNotFound("The model exists but it has not a version with id:" + str(version_id))
    # Returning model information and version paired with training information
    return model_info,versions_and_info


def get_trained_model_feature_schema(trained_model_id: int, session: SessionDep) -> list[dict[str,SQLModel]]:
    # The feature schema primary key is based as a ternary (trained_model_id,data_type_id,feature_pos)
    # So for a given trained model, we just query the Feature Schema table for the trained_model_id
    # A further join is done so that we get also the name of the feature
    statement = select(FeatureSchema, DataType).join(DataType).where(FeatureSchema.trained_model_id == trained_model_id)
    results = session.exec(statement).all()
    # Building payload as docs dictate
    data_list = []
    for feature,data_type in results:
        data_list.append({"column_name":feature.feature_name,"categorical":data_type.is_categorical,
                          "column_datatype":data_type.type,"column_position":feature.feature_position})
    return data_list

def delete_trained_model_schemas(trained_model: TrainedModel, session: SessionDep):

    statement = select(FeatureSchema).where(FeatureSchema.trained_model_id == trained_model.id)
    results = session.exec(statement).all()
    for result in results:
        session.delete(result)
    session.commit()


def delete_trained_model_version(trained_model: TrainedModel,version_id: int, session: SessionDep):
    if version_id is None:
        statement = select(ModelVersion,TrainingInfo).join(TrainingInfo).where(ModelVersion.trained_model_id == trained_model.id)
    else:
        statement = select(ModelVersion,TrainingInfo).join(TrainingInfo).where(ModelVersion.trained_model_id == trained_model.id)\
            .where(ModelVersion.id == version_id)
    results = session.exec(statement).all()
    return results

def get_models_and_versions(session: SessionDep) -> list:
    statement = select(TrainedModel,ModelVersion).outerjoin(ModelVersion)
    results = session.exec(statement).all()
    payload = {}
    for result in results:
        model = payload.get(result[0].id)
        if not model and result[1]:
            payload.update({result[0].id:{"name":result[0].name,
                                          "id": result[0].id,
                                          "dataset_name": result[0].dataset_name,
                                          "input_shape":result[0].input_shape,
                                          "algorithm_name":result[0].algorithm_name,
                                          "size":result[0].size,
                                          "version_ids":[result[1].id]}})
        elif not model:
            payload.update({result[0].id:{"name":result[0].name,
                                          "id": result[0].id,
                                          "dataset_name": result[0].dataset_name,
                                          "input_shape":result[0].input_shape,
                                          "algorithm_name":result[0].algorithm_name,
                                          "size":result[0].size,
                                          "version_ids":[]}})
        else:
            model["version_ids"].append(result[1].id)
    return list(payload.values())

def get_all(session: SessionDep) -> list[TrainedModel]:
    statement = select(TrainedModel)
    results = session.exec(statement)
    return results.all()

def get_by_id(model_id: int,session: SessionDep):
    statement = select(TrainedModel).where(TrainedModel.id == model_id)
    train_model = session.exec(statement).one()
    return train_model

def save_model(model: TrainedModel,session: SessionDep, refresh: bool = False) -> None:
    session.add(model)
    session.commit()
    if refresh:
        session.refresh(model)

