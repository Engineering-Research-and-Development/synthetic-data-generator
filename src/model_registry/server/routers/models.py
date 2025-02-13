from fastapi import APIRouter
from ..routers import algorithm, trained_models

router = APIRouter(prefix="/models", tags=['All models'])

# The following functions will serve as the mains interface for the client layer
@router.get("/",
            name="Get all the algorithms and trained model in the registry",
            summary="This function returns all the algorithm and trained models present in the registry")
async def controller_get_all_models() -> dict:
    """
    This function represent the main interface for client layer, and it returns all the models present in the repository.
    :return: A dictionary containing a list of System Models and Trained Models present in the repository
    """
    algorithms = await algorithm.get_all_algorithms_datatypes()
    train_models = await trained_models.get_trained_models_and_versions()
    return {"algorithms":algorithms , "trained_models":train_models}

