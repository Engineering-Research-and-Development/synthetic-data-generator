
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from model_registry.validation.valschema import CreateTrainedModel, CreateModelVersion, CreateTrainingInfo,CreateFeatureSchema
from model_registry.database.handlers import tm_handler as db_handler
from model_registry.database.handlers import fs_handler as db_feature_handler
from model_registry.database.handlers import tr_info_handler as db_info_handler
from model_registry.database.handlers import mv_handler as db_model_version_handler
from model_registry.validation.handlers import tm_valhandler,fs_valhandler,tr_info_valhandler,mv_valhandler
from model_registry.server.dependencies import SessionDep
from model_registry.server.errors import NoVersions, NoModelFound, VersionNotFound


router = APIRouter(prefix="/trained_models")



@router.get("/", status_code=200)
async def get_all_trained_models(session: SessionDep):
    return db_handler.get_all(session)

@router.get("/versions", status_code=200)
async def get_trained_models_and_versions(session: SessionDep):
    models = db_handler.get_models_and_versions(session)
    return models

@router.get("/{trained_model_id}", status_code=200)
async def get_trained_model_id(trained_model_id: int, session: SessionDep):
    try:
        train_model = db_handler.get_by_id(trained_model_id,session)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No trained instance with id: " + str(trained_model_id) + " has been found")
    return train_model

@router.get("/{trained_model_id}/versions", status_code=200)
async def get_all_train_model_versions(trained_model_id: int, session: SessionDep,version_id: int | None = None):
    try:
        model_info, version_and_train = db_handler.get_trained_model_versions(trained_model_id, version_id, session)
    except NoModelFound as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except NoVersions as e:
        raise HTTPException(status_code=404, detail=f"{e}")

    feature_schema = db_handler.get_trained_model_feature_schema(trained_model_id, session)
    payload = {"model": model_info, "versions": version_and_train, "feature_schema": feature_schema}
    return payload

@router.post("/", status_code=201)
async def create_model_and_version(trained_model: CreateTrainedModel, version: CreateModelVersion, training_info: CreateTrainingInfo, feature_schema: list[CreateFeatureSchema], session: SessionDep):
    validated_model = tm_valhandler.validate_model(trained_model)
    try:
        db_handler.save_model(validated_model,session,refresh=True)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="The value of algorithm_name must be a valid system model. No system model with such value is present")

    try:
        validated_features = fs_valhandler.validate_all_schemas(feature_schema)
    except NoResultFound:
        raise HTTPException(status_code=400, detail="This kind of datatype is not supported. Please add it to use it")

    for feature in validated_features:
        feature.trained_model_id = validated_model.id
    db_feature_handler.save_all_features(validated_features,session)

    validated_training_info = tr_info_valhandler.validate_model(training_info)
    db_info_handler.save_model(validated_training_info,session,refresh=True)

    validated_version = mv_valhandler.validate_model(version)
    validated_version.training_info_id = validated_training_info.id
    validated_version.trained_model_id = validated_model.id

    db_model_version_handler.save_model(validated_version,session)

    return {"message": "Successfully saved model with the following id", "id": validated_model.id}

@router.delete("/{trained_model_id}", status_code=200)
async def delete_train_model(trained_model_id: int, session: SessionDep):
    try:
        train_model = db_handler.get_by_id(trained_model_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No trained instance with id: " + str(trained_model_id) + " has been found")
    db_handler.delete_trained_model_schemas(train_model, session)
    try:
        _, versions_infos = db_handler.get_trained_model_versions(model_id=trained_model_id, session=session, version_id=None)
    except NoModelFound as e:
        raise HTTPException(status_code=404, detail=f"{e}")
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
async def delete_train_model_version(trained_model_id: int,session: SessionDep, version_id: int | None = None):
    try:
        _, version_info = db_handler.get_trained_model_versions(trained_model_id, version_id, session)
    except (NoModelFound,NoVersions,VersionNotFound) as e:
        raise HTTPException(status_code=404, detail=f"{e}")

    for elem in version_info:
        session.delete(elem["version_info"])
        session.delete(elem["training_info"])
    session.commit()