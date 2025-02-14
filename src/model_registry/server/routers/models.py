from fastapi import APIRouter
from ..routers import algorithm, trained_models
from server.database.validation.schema import AlgorithmsAndTrainedModels

router = APIRouter(prefix="/models", tags=['All models'])

# The following functions will serve as the mains interface for the client layer
@router.get("/",
            name="Get all the algorithms and trained model in the registry",
            summary="This function returns all the algorithm and trained models present in the registry",
            description="This returns all the algorithms and trained models present in the registry"
                        " , the algorithms will have the allowed datatypes while the trained model will also have a list"
                        " of all their version ids")
async def controller_get_all_models() -> AlgorithmsAndTrainedModels:
    algorithms = await algorithm.get_all_algorithms(include_allowed_datatypes=True)
    train_models = await trained_models.get_all_trained_models(include_version_ids=True)
    return AlgorithmsAndTrainedModels(algorithms=algorithms , trained_models=train_models)

