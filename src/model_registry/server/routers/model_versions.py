from fastapi import APIRouter
from starlette.responses import JSONResponse
from ..database.validation.schema import ModelVersion as PydanticModelVersion
from ..database.schema import ModelVersion
from peewee import DoesNotExist

router = APIRouter(prefix="/versions", tags=['Model Versions'])


@router.get("/",
            status_code=200,
            name="Get all the trained model versions in the model registry")
async def get_all_model_versions() -> list[PydanticModelVersion]:
    """
    ## Get All Trained Model Versions

    ### Endpoint
    **GET** `/`

    ### Name
    **Get all the trained model versions in the model registry**

    ### Summary
    Retrieves a list of all trained model versions available in the model registry.

    ### Response
    - **200 OK**: Returns a list of trained model versions.

    #### Response Body (Success)
    ```json
    [
      {
        "id": 1,
        "name": "ModelA",
        "version": "1.0",
        "created_at": "2024-01-01T12:00:00Z"
      },
      {
        "id": 2,
        "name": "ModelB",
        "version": "2.1",
        "created_at": "2024-02-10T15:30:00Z"
      }
    ]

    """
    return [PydanticModelVersion(**row) for row in ModelVersion.select().dicts()]

@router.get("/{version_id}",
            status_code=200,
            name="Get a version by id",
            summary="It returns a specific model version given his id",
            response_model=PydanticModelVersion)
async def get_version_by_id(version_id: int):
    """
     ## Get a Model Version by ID

    ### Endpoint
    **GET** `/{version_id}`

    ### Name
    **Get a version by ID**

    ### Summary
    Retrieves a specific model version given its ID.

    ### Path Parameter
    | Name       | Type  | Description                                | Example |
    |-----------|------|--------------------------------------------|---------|
    | version_id | `int` | The ID of the model version to retrieve | `1` |

    ### Response
    - **200 OK**: Returns the requested model version.
    - **404 Not Found**: If the model version with the specified ID does not exist.

    #### Response Body (Success)
    ```json
    {
      "id": 1,
      "name": "ModelA",
      "version": "1.0",
      "created_at": "2024-01-01T12:00:00Z"
    }

    """
    try:
        version = ModelVersion.select().where(ModelVersion.id == version_id).dicts().get()
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message":"No version with id: " + str(version_id) + " has been found"})
    return PydanticModelVersion(**version)

