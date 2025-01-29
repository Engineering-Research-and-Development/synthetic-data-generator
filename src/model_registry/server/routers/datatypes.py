import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.schema import DataType
from database.validation.schema import DataType as PydanticDataType
from playhouse.shortcuts import model_to_dict

router = APIRouter(prefix="/datatypes")


@router.get("/",
            name="Get all datatypes",
            summary="Get all the available datatypes",
            )
async def get_all_datatypes() -> list[PydanticDataType]:
    results = [datatype for datatype in DataType.select().dicts()]
    return results


@router.get("/{datatype_id}",
            name="Get a single datatype",
            summary="Select a single datatype",
            response_model= PydanticDataType,
            responses={404: {"model": str}}
            )
async def get_single_datatype(datatype_id: int = Path(description="The id of the datatype you want to get", example=1)):
    try:
        result = DataType.get_by_id(datatype_id).get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

    return model_to_dict(result)
