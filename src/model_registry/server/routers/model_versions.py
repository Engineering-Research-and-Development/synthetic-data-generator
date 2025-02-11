from fastapi import APIRouter
from starlette.responses import JSONResponse
from src.model_registry.server.database.validation.schema import ModelVersion as PydanticModelVersion
from src.model_registry.server.database.schema import ModelVersion
from peewee import DoesNotExist

router = APIRouter(prefix="/versions")


@router.get("/",
            status_code=200,
            name="Get all the trained model versions in the model registry")
async def get_all_model_versions() -> list[PydanticModelVersion]:
    return [PydanticModelVersion(**row) for row in ModelVersion.select().dicts()]

@router.get("/{version_id}",
            status_code=200,
            name="Get a version by id",
            summary="It returns a specific model version given his id",
            response_model=PydanticModelVersion)
async def get_version_by_id(version_id: int):
    try:
        version = ModelVersion.select().where(ModelVersion.id == version_id).dicts().get()
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message":"No version with id: " + str(version_id) + " has been found"})
    return PydanticModelVersion(**version)

@router.post("/{trained_model_id}",
             status_code=201,
             name="It creates a model version and training info and it adds it to the trained_model_id")
# This method should be discussed
def create_version_and_info(trained_model_id: int):
    raise NotImplemented("This method has not yet implemented")