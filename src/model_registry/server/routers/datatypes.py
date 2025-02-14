import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from ..database.schema import DataType
from ..database.validation.schema import CreateDataType,DataType as PydanticDataType


router = APIRouter(prefix="/datatypes", tags=['Datatypes'])


@router.get("/",
            name="Get all datatypes",
            summary="Get all the available datatypes",
            )
async def get_all_datatypes() -> list[PydanticDataType]:
    """
    ## Get All Datatypes

    ### Endpoint
    **GET** `/`

    ### Name
    **Get all datatypes**

    ### Summary
    Retrieves all the available datatypes.

    ### Response
    - **200 OK**: Returns a list of all available datatypes.

    #### Response Body
    A JSON array of objects representing datatypes.

    ```json
    [
      {
        "id": 1,
        "name": "ExampleType",
        "description": "This is an example datatype"
      },
      {
        "id": 2,
        "name": "AnotherType",
        "description": "Another example datatype"
      }
    ]

    """
    results = [PydanticDataType(**datatype) for datatype in DataType.select().dicts()]
    return results


@router.get("/{datatype_id}",
            name="Get a single datatype",
            summary="Select a single datatype",
            response_model= PydanticDataType,
            responses={404: {"model": str}}
            )
async def get_single_datatype(datatype_id: int = Path(description="The id of the datatype you want to get", examples=1)):
    """
    ## Get a Single Datatype

    ### Endpoint
    **GET** `/{datatype_id}`

    ### Name
    **Get a single datatype**

    ### Summary
    Retrieves a specific datatype by its ID.

    ### Path Parameter
    | Name        | Type  | Description                      | Example |
    |------------|------|----------------------------------|---------|
    | datatype_id | `int` | The ID of the datatype to retrieve | `1` |

    ### Response
    - **200 OK**: Returns the requested datatype as a `PydanticDataType` object.
    - **404 Not Found**: If the datatype with the specified ID does not exist.

    #### Response Body (Success)
    ```json
    {
      "id": 1,
      "name": "ExampleType",
      "description": "This is an example datatype"
    }

    """
    try:
        result = DataType.select().where(DataType.id == datatype_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return PydanticDataType(**result)

@router.post("/",
             status_code=201,
             name="Create a datatype",
             summary="Given the data it creates a datatype that can be used across the registry")
def create_datatype(datatype: CreateDataType):
    """
        ## Create a Datatype

        ### Endpoint
        **POST** `/`

        ### Name
        **Create a datatype**

        ### Summary
        Creates a new datatype that can be used across the registry.

        ### Request Body
        The request must include a JSON object that follows the `CreateDataType` model.

        #### Example Request Body
        ```json
        {
          "name": "ExampleType",
          "description": "This is an example datatype"
        }

    """
    DataType.insert(**datatype.model_dump()).execute()
