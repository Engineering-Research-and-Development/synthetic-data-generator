from fastapi import APIRouter
from starlette.responses import JSONResponse
from ..database.schema import TrainingInfo
from ..database.validation.schema import TrainingInfo as PydanticTrainingInfo
from peewee import DoesNotExist

router = APIRouter(prefix="/training_info", tags=['Training Info'])

@router.get("/{training_info_id}",
            status_code=200,
            name="Get training info by id",
            summary="It returns a training info given the id",
            responses={404:{"model":str}},
            response_model=PydanticTrainingInfo)
async def get_trained_info(training_info_id: int):
    """
    ## Get Training Info by ID

    ### Endpoint
    **GET** `/{training_info_id}`

    ### Name
    **Get training info by id**

    ### Summary
    Returns training information associated with a specific ID.

    ### Path Parameter
    | Name               | Type  | Description                                                   | Example |
    |-------------------|-------|---------------------------------------------------------------|---------|
    | training_info_id  | `int` | The ID of the training information to retrieve                | `1`     |

    ### Response
    - **200 OK**: Returns the requested training information.
    - **404 Not Found**: If no training information is found with the specified ID.

    #### Response Body (Success)
    ```json
    {
      "id": 1,
      "algorithm_id": 2,
      "training_date": "2024-01-01",
      "performance_metrics": {"accuracy": 0.95}
    }

    """
    try:
        train_info = TrainingInfo.select().where(TrainingInfo.id == training_info_id).dicts().get()
    except DoesNotExist:
        return JSONResponse(status_code=404, content={"message":"No training info with id: " + str(training_info_id) + " has been found"})
    return PydanticTrainingInfo(**train_info)

