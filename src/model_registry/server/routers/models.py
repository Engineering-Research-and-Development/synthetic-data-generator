from fastapi import APIRouter
from ..routers import algorithm, trained_models

router = APIRouter(prefix="/models", tags=['All models'])

# The following functions will serve as the mains interface for the client layer
@router.get("/",
            name="Get all the algorithms and trained model in the registry",
            summary="This function returns all the algorithm and trained models present in the registry")
async def controller_get_all_models() -> dict:
    """
    ## Get All Algorithms and Trained Models
    ### Endpoint
    **GET** `/`

    ### Name
    **Get all the algorithms and trained models in the registry**

    ### Summary
    Retrieves all algorithms and trained models present in the registry.

    ### Response
    - **200 OK**: Returns a dictionary containing all algorithms and trained models.

    #### Response Body (Success)
    ```json
    {
      "algorithms": [
        {
          "id": 1,
          "name": "AlgorithmA",
          "description": "A sample algorithm"
        },
        {
          "id": 2,
          "name": "AlgorithmB",
          "description": "Another sample algorithm"
        }
      ],
      "trained_models": [
        {
          "id": 101,
          "name": "ModelA",
          "version": "1.0",
          "created_at": "2024-01-01T12:00:00Z"
        },
        {
          "id": 102,
          "name": "ModelB",
          "version": "2.1",
          "created_at": "2024-02-10T15:30:00Z"
        }
      ]
    }

    """
    algorithms = await algorithm.get_all_algorithms(include_allowed_datatypes=True)
    train_models = await trained_models.get_all_trained_models(include_version_ids=True)
    return {"algorithms":algorithms , "trained_models":train_models}

