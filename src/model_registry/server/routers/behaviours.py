import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.schema import Behaviour
from database.validation.schema import Behaviour as PydanticBehaviour

router = APIRouter(prefix="/behaviours")


@router.get("/",
            name="Get all behaviours",
            summary="Get all the available behaviours",
            )
async def get_all_behaviours() -> list[PydanticBehaviour]:
    results = [behaviour for behaviour in Behaviour.select().dicts()]
    return results


@router.get("/{behaviour_id}",
            name="Get a single behaviour",
            summary="Select a single behaviour",
            response_model= PydanticBehaviour,
            responses={404: {"model": str}}
            )
async def get_single_behaviour(behaviour_id: int = Path(description="The id of the behaviour you want to get", example=1)):
    try:
        result = Behaviour.get_by_id(behaviour_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Item not found"})

    return result
