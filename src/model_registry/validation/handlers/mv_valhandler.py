from model_registry.validation.valschema import CreateModelVersion
from model_registry.database.schema import ModelVersion

def validate_model(in_model: CreateModelVersion) -> ModelVersion:
    return ModelVersion.model_validate(in_model)