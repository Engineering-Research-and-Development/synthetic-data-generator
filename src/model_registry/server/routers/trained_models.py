from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select
from model_registry.database.schema import TrainedModel, ModelVersion, TrainingInfo
from model_registry.database.validation import CreateTrainedModel, CreateModelVersion, CreateTrainingInfo, CreateFeatureSchema
from model_registry.server.errors import NoVersions
from ..dependencies import SessionDep
from model_registry.server.service import tm_service as service

router = APIRouter(prefix="/trained_models")

@router.get("/", status_code=200)
async def get_all_trained_models(session: SessionDep):
    statement = select(TrainedModel)
    results = session.exec(statement)
    return results.all()

@router.get("/versions", status_code=200)
async def get_trained_models_and_versions(session: SessionDep):
    models = service.get_models_and_versions(session)
    return models

@router.get("/{trained_model_id}", status_code=200)
async def get_trained_model_id(trained_model_id: int, session: SessionDep):
    try:
        statement = select(TrainedModel).where(TrainedModel.id == trained_model_id)
        train_model = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No trained instance with id: " + str(trained_model_id) + " has been found")
    return train_model

@router.get("/{trained_model_id}/versions", status_code=200)
async def get_all_train_model_versions(trained_model_id: int, version_id: int, session: SessionDep):
    try:
        model_info, version_and_train = service.get_trained_model_versions(trained_model_id, version_id, session)
    except NoVersions as e:
        raise HTTPException(status_code=404, detail=f"{e}")

    feature_schema = service.get_trained_model_feature_schema(trained_model_id, session)
    payload = {"model": model_info, "versions": version_and_train, "feature_schema": feature_schema}
    return payload

@router.post("/", status_code=201)
async def create_model_and_version(trained_model: CreateTrainedModel, version: CreateModelVersion, training_info: CreateTrainingInfo, feature_schema: list[CreateFeatureSchema], session: SessionDep):
    validated_model = TrainedModel.model_validate(trained_model)
    try:
        session.add(validated_model)
        session.commit()
        session.refresh(validated_model)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The value of algorithm_name must be a valid system model. No system model with such value is present")

    try:
        validated_features = service.validate_all_schemas(feature_schema, session)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="This kind of datatype is not supported. Please add it to use it")

    for feature in validated_features:
        feature.trained_model_id = validated_model.id


    for feature in validated_features:
        session.add(feature)
    session.commit()
    validated_training_info = TrainingInfo.model_validate(training_info)

    session.add(validated_training_info)
    session.commit()
    session.refresh(validated_training_info)
    validated_version = ModelVersion.model_validate(version)
    validated_version.training_info_id = validated_training_info.id
    validated_version.trained_model_id = validated_model.id

    session.add(validated_version)
    session.commit()
    return {"message": "Successfully saved model with the following id", "id": validated_model.id}

@router.delete("/{trained_model_id}", status_code=200)
async def delete_train_model(trained_model_id: int, session: SessionDep):
    try:
        statement = select(TrainedModel).where(TrainedModel.id == trained_model_id)
        train_model = session.exec(statement).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No trained instance with id: " + str(trained_model_id) + " has been found")
    service.delete_trained_model_schemas(train_model, session)

    try:
        _, versions_infos = service.get_trained_model_versions(model_id=trained_model_id, session=session, version_id=None)
    except NoVersions:
        pass
    else:
        for elem in versions_infos:
            session.delete(elem["version_info"])
            session.delete(elem["training_info"])
        session.commit()

    session.delete(train_model)
    session.commit()

@router.delete("/{trained_model_id}/versions", status_code=200)
async def delete_train_model_version(trained_model_id: int, version_id: int, session: SessionDep):
    try:
        _, version_info = service.get_trained_model_versions(trained_model_id, version_id, session)
    except NoVersions as e:
        raise HTTPException(status_code=404, detail=f"{e}")

    for elem in version_info:
        session.delete(elem["version_info"])
        session.delete(elem["training_info"])
    session.commit()