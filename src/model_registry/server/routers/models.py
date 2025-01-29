from fastapi import APIRouter
from model_registry.server.dependencies import SessionDep
from model_registry.server.routers import system_models, trained_models

router = APIRouter(prefix="/models")

# The following functions will serve as the mains interface for the client layer
@router.get("/")
async def controller_get_all_models(session: SessionDep) -> dict:
    """
    This function represent the main interface for client layer, and it returns all the models present in the repository.
    :return: A dictionary containing a list of System Models and Trained Models present in the repository
    """
    sys_models = await system_models.get_all_system_models(session)
    train_models = await trained_models.get_trained_models_and_versions(session)
    return {"built_in":sys_models , "trained_models":train_models}

