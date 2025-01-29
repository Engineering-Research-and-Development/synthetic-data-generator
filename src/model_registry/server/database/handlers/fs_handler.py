from model_registry.database.schema import FeatureSchema
from model_registry.server.dependencies import SessionDep

def save_all_features(features: list[FeatureSchema],session: SessionDep) -> None:
    for feature in features:
        session.add(feature)
    session.commit()