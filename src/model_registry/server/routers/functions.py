import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from ..database.schema import Parameter, Function, FunctionParameter
from ..database.validation.schema import FunctionParameterOut

router = APIRouter(prefix="/functions", tags=['Functions'])


@router.get("/",
            name="Get all function parameters",
            summary="Get all the available function parameters",
            response_model=list[FunctionParameterOut],
            )
async def get_all_functions() -> list[FunctionParameterOut]:
    """
    ## Get All Function Parameters

    ### Endpoint
    **GET** `/`

    ### Name
    **Get all function parameters**

    ### Summary
    Retrieves all available functions along with their associated parameters.

    ### Response
    - **200 OK**: Returns a list of functions, each with its associated parameters.

    #### Response Body (Success)
    ```json
    [
      {
        "function": {
          "id": 1,
          "name": "ExampleFunction",
          "description": "This is an example function"
        },
        "parameter": [
          {
            "id": 101,
            "name": "Parameter1",
            "type": "string"
          },
          {
            "id": 102,
            "name": "Parameter2",
            "type": "integer"
          }
        ]
      },
      {
        "function": {
          "id": 2,
          "name": "AnotherFunction",
          "description": "Another example function"
        },
        "parameter": [
          {
            "id": 201,
            "name": "ParameterA",
            "type": "boolean"
          }
        ]
      }
    ]

    """
    functions = Function.select().dicts()
    results = [
        FunctionParameterOut(
            function=function,
            parameter=[Parameter.select().where(Parameter.id == p.parameter).dicts().get() for p in FunctionParameter.select().where(FunctionParameter.function == function['id'])]
        )
        for function in functions
    ]

    return results


@router.get("/{function_id}",
            name="Get function parameters by function ID",
            summary="Get all parameters associated with a specific function",
            response_model=FunctionParameterOut,
            responses={404: {"model": str}}
            )
async def get_function_parameters_by_function_id(
        function_id: int = Path(description="The ID of the function to retrieve parameters for", examples=1)
):
    """
    ## Get Function Parameters by Function ID

    ### Endpoint
    **GET** `/{function_id}`

    ### Name
    **Get function parameters by function ID**

    ### Summary
    Retrieves all parameters associated with a specific function.

    ### Path Parameter
    | Name        | Type  | Description                                       | Example |
    |------------|------|---------------------------------------------------|---------|
    | function_id | `int` | The ID of the function to retrieve parameters for | `1` |

    ### Response
    - **200 OK**: Returns the function details along with its associated parameters.
    - **404 Not Found**: If the function with the specified ID does not exist.

    #### Response Body (Success)
    ```json
    {
      "function": {
        "id": 1,
        "name": "ExampleFunction",
        "description": "This is an example function"
      },
      "parameter": [
        {
          "id": 101,
          "name": "Parameter1",
          "type": "string"
        },
        {
          "id": 102,
          "name": "Parameter2",
          "type": "integer"
        }
      ]
    }

    """
    try:
        function = Function.select().where(Function.id == function_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Function not found"})

    parameters = [Parameter.select().where(Parameter.id == p.parameter).dicts().get() for p in FunctionParameter.select().where(FunctionParameter.function == function_id)]

    return FunctionParameterOut(function=function, parameter=parameters)