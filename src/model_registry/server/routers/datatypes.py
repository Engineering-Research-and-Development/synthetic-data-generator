import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.schema import DataType
from database.validation.schema import DataType as PydanticDataType
from database.handlers import dt_handler as db_handler

router = APIRouter(prefix="/datatypes")


@router.get("/",
            name="Get all datatypes",
            summary="Get all the available datatypes",
            )
async def get_all_datatypes() -> list[PydanticDataType]:
    results = [datatype for datatype in DataType.select().dicts().get()]
    return results


@router.get("/{datatype_id}",
            name="Get a single datatype",
            summary="Select a single datatype",
            response_model= PydanticDataType,
            responses={404: {"model": str}}
            )
async def get_single_datatype(datatype_id: int = Path(description="The id of the datatype you want to get", example=1)):
    try:
        result = DataType.select().where(DataType.id == datatype_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
    return PydanticDataType(**result)
