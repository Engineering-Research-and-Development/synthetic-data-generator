from model_registry.database.handlers import dt_handler
from model_registry.validation.handlers import dt_valhander
from model_registry.validation.valschema import CreateFeatureSchema

def validate_all_schemas(features: list[CreateFeatureSchema]) -> list:
    payload = []
    for feature in features:
        # For each feature we need to search the id since it is not passed in input
        # And we need to check that is present in the db (it means we allow it)
        datatype_id = dt_handler.get_id_by_type_and_categorical(feature.datatype,feature.is_categorical)
        validated_feature = dt_valhander.validate_model(feature)
        validated_feature.datatype_id = datatype_id
        payload.append(validated_feature)
    return payload