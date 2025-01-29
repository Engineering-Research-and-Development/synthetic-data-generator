from model_registry.validation.valschema import CreateSystemModel
from model_registry.database.schema import SystemModel

def validate_model(in_model: CreateSystemModel) -> SystemModel:
    return SystemModel.model_validate(in_model)