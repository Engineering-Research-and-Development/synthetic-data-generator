"""The service layer should be responsible for implementing the business logic of our application by communicating
with the model layer. """
from model_registry.database.schema import TrainedModel, TrainingInfo, ModelVersion, FeatureSchema, DataType
from model_registry.database.model import engine,Session
from sqlmodel import select, join, SQLModel

from model_registry.server.validation import CreateFeatureSchema


def get_trained_model_versions(model_id,version_id: int | None = None) -> tuple[SQLModel,dict]:
    with Session(engine) as session:
        if version_id is None:
            statement = select(ModelVersion,TrainedModel,TrainingInfo).join(TrainedModel).join(TrainingInfo).where(TrainedModel.id == model_id)
        else:
            statement = select(ModelVersion,TrainedModel,TrainingInfo).join(TrainedModel).join(TrainingInfo).where(TrainedModel.id == model_id)\
                .where(ModelVersion.id == version_id)
        results = session.exec(statement).all()

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
        data_list.append({"column_name":feature.feature_name,"categorical":feature.is_categorical,
                          "column_datatype":data_type.type,"feature_position":feature.feature_position})
    return data_list


def validate_all_schemas(features: list[CreateFeatureSchema]) -> list[FeatureSchema]:
    payload = []
    for feature in features:
        payload.append(FeatureSchema.model_validate(feature))
    return payload

