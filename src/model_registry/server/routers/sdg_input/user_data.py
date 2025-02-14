import os

import requests
from fastapi import APIRouter
from starlette.responses import JSONResponse

from .handlers import check_function_parameters, check_user_file, check_ai_model
from .schema import UserDataInput, GeneratorDataOutput

router = APIRouter(prefix="/sdg_input", tags=['SDG Input'])

generator_url = os.environ.get("generator_url", "http://localhost:8010")

@router.post("/",
             name="Synthetic Data Generator input collection",
             responses={400: {"model": str},
                        500: {"model": str}}
             )
async def collect_user_input(input_data: UserDataInput):
    """
    ## Synthetic Data Generator Input Collection

    ### Endpoint
    **POST** `/`

    ### Name
    **Synthetic Data Generator input collection**

    ### Description
    This endpoint collects the required information and initiates the Synthetic Data Generator process using the provided data. The input data may include functions, AI model details, and an optional user file for dataset augmentation.

    ### Request Body
    The request body must include the following information:

    - **functions**: A list of function IDs used for data generation.
    - **ai_model**: Details of the AI model, including whether it is a new model or requires fine-tuning.
    - **user_file**: An optional file from the user for dataset augmentation.
    - **additional_rows**: The number of additional rows to generate.

    #### Example Request Body
    ```json
    {
      "functions": [1, 2, 3],
      "ai_model": {
        "name": "AI_Model_X",
        "new_model": true
      },
      "user_file": "user_data.csv",
      "additional_rows": 100
    }

    """
    data = input_data.model_dump()

    function_ids = check_function_parameters(data['functions'])
    if not function_ids:
        return JSONResponse(status_code=400, content="Error analysing functions")

    model = check_ai_model(data.get('ai_model'))
    if not model:
        return JSONResponse(status_code=400, content="Wrong model")

    body={}
    if data.get('user_file') is not None:
        user_file = check_user_file(data.get('user_file'))
        if not user_file:
            return JSONResponse(status_code=400, content="Error parsing input dataset")

        body=GeneratorDataOutput(
                            function_ids=function_ids,
                            n_rows=data.get('additional_rows'),
                            model=model,
                            dataset=user_file,
                            )

    if data.get('ai_model').get('new_model'):
        url=generator_url+"/train"
    else:
        url=generator_url+"/fine_tune"

    response = requests.post(url, json=body.model_dump())
    if response.status_code == 200:
        return JSONResponse(status_code=200, content="Data augmentation started")
    else:
        return JSONResponse(status_code=500, content=response.reason)


