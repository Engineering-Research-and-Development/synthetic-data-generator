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
    This method returns all the datatypes that are present in the model registry
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
    This method returns a datatype given his id. If not present, an 404 error will be returned
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
        This method given the information of a datatype it creates it.
    """
    DataType.insert(**datatype.model_dump()).execute()
