"""The service layer should be responsible for implementing the business logic of our application by communicating
with the model layer. """
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from model_registry.database.schema import TrainedModel, TrainingInfo, ModelVersion, FeatureSchema, DataType
from model_registry.database.model import engine,Session
from sqlmodel import select, SQLModel
from model_registry.database.validation import CreateFeatureSchema
from model_registry.server.errors import NoVersions


def get_trained_model_versions(model_id,version_id: int | None = None) -> tuple[SQLModel,dict]:
    with Session(engine) as session:
        if version_id is None:
            statement = select(ModelVersion,TrainedModel,TrainingInfo).join(TrainedModel).join(TrainingInfo).where(TrainedModel.id == model_id)
        else:
            statement = select(ModelVersion,TrainedModel,TrainingInfo).join(TrainedModel).join(TrainingInfo).where(TrainedModel.id == model_id)\
                .where(ModelVersion.id == version_id)
        results = session.exec(statement).all()
    if len(results) == 0 :
        raise NoVersions("This trained model exists but has no versions!")
    version_and_info = [{"version_info":elem[0],"training_info":elem[2]} for elem in results]
    model_info = results[0][1]
    # Returning model information and version paired with training information
    return model_info,version_and_info

def get_trained_model_feature_schema(trained_model_id: int) -> list[dict[str,SQLModel]]:
    # The feature schema primary key is based as a ternary (trained_model_id,data_type_id,feature_pos)
    # So for a given trained model, we just query the Feature Schema table for the trained_model_id
    # A further join is done so that we get also the name of the feature
    with Session(engine) as session:
        statement = select(FeatureSchema, DataType).join(DataType).where(FeatureSchema.trained_model_id == trained_model_id)
        results = session.exec(statement).all()
    # Building payload as docs dictate
    data_list = []
    for feature,data_type in results:
        data_list.append({"column_name":feature.feature_name,"categorical":data_type.is_categorical,
                          "column_datatype":data_type.type,"column_position":feature.feature_position})
    return data_list

def validate_all_schemas(features: list[CreateFeatureSchema]) -> list[FeatureSchema]:
    payload = []
    with Session(engine) as session:
        for feature in features:
            # For each feature we need to search the id since it is not passed in input
            statement = select(DataType.id).where(DataType.type == feature.datatype)
            result = session.exec(statement).one()
            validated_feature = FeatureSchema.model_validate(feature)
            validated_feature.datatype_id = result
            payload.append(validated_feature)
    return payload

def delete_trained_model_schemas(trained_model: TrainedModel):
    with Session(engine) as session:
        statement = select(FeatureSchema).where(FeatureSchema.trained_model_id == trained_model.id)
        results = session.exec(statement).all()
        for result in results:
            session.delete(result)
        session.commit()


def delete_trained_model_version(trained_model: TrainedModel,version_id: int | None = None):
    with Session(engine) as session:
        if version_id is None:
            statement = select(ModelVersion,TrainingInfo).join(TrainingInfo).where(ModelVersion.trained_model_id == trained_model.id)
        else:
            statement = select(ModelVersion,TrainingInfo).join(TrainingInfo).where(ModelVersion.trained_model_id == trained_model.id)\
                .where(ModelVersion.id == version_id)
        results = session.exec(statement).all()
        return results

def get_models_and_versions() -> list:
    with Session(engine) as session:
        statement = select(TrainedModel,ModelVersion).join(ModelVersion)
        results = session.exec(statement).all()
    payload = {}
    for result in results:
        model = payload.get(result[0].id)
        if model is None:
            payload.update({result[0].id:{"name":result[0].name,
                                          "id": result[0].id,
                                          "dataset_name": result[0].dataset_name,
                                          "input_shape":result[0].input_shape,
                                          "algorithm_name":result[0].algorithm_name,
                                          "size":result[0].size,
                                          "version_ids":[result[1].id]}})
        else:
            model["version_ids"].append(result[1].id)
    return list(payload.values())
