from fastapi import APIRouter
from starlette.responses import JSONResponse
from src.model_registry.server.database.schema import TrainingInfo
from src.model_registry.server.database.validation.schema import TrainingInfo as PydanticTrainingInfo
from peewee import DoesNotExist

router = APIRouter(prefix="/training_info")

@router.get("/{training_info_id}",
            status_code=200,
            name="Get training info by id",
            summary="It returns a training info given the id",
            responses={404:{"model":str}},
            response_model=PydanticTrainingInfo)
async def get_trained_info(training_info_id: int):
    try:
        train_info = TrainingInfo.select().where(TrainingInfo.id == training_info_id).dicts().get()
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message":"No training info with id: " + str(training_info_id) + " has been found"})
    return PydanticTrainingInfo(**train_info)

