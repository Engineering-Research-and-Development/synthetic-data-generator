from model_registry.validation.valschema import CreateTrainedModel
from model_registry.database.schema import TrainedModel


def validate_model(in_model: CreateTrainedModel) -> TrainedModel:
    return TrainedModel.model_validate(in_model)