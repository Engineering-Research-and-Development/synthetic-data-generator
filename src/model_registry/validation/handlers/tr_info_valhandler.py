from model_registry.validation.valschema import CreateTrainingInfo
from model_registry.database.schema import TrainingInfo

def validate_model(train_info: CreateTrainingInfo) -> TrainingInfo:
    return TrainingInfo.model_validate(train_info)