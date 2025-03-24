import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.schema import Parameter, Function, FunctionParameter
from database.validation.schema import FunctionParameterOut

router = APIRouter(prefix="/functions", tags=["Functions"])


@router.get(
    "/",
    name="Get all function parameters",
    summary="Get all the available function parameters",
    response_model=list[FunctionParameterOut],
)
async def get_all_functions() -> list[FunctionParameterOut]:
    """
    This method returns all the function parameters that are present in the model registry
    """
    functions = Function.select().dicts()
    results = [
        FunctionParameterOut(
            function=function,
            parameter=[
                Parameter.select().where(Parameter.id == p.parameter).dicts().get()
                for p in FunctionParameter.select().where(
                    FunctionParameter.function == function["id"]
                )
            ],
        )
        for function in functions
    ]

    return results


@router.get(
    "/{function_id}",
    name="Get function parameters by function ID",
    summary="Get all parameters associated with a specific function",
    response_model=FunctionParameterOut,
    responses={404: {"model": str}},
)
async def get_function_parameters_by_function_id(
    function_id: int = Path(
        description="The ID of the function to retrieve parameters for", examples=[1]
    ),
):
    """
    This function returns a function parameter given his id. If not found, a 404 will be returned
    """
    try:
        function = Function.select().where(Function.id == function_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Function not found"})

    parameters = [
        Parameter.select().where(Parameter.id == p.parameter).dicts().get()
        for p in FunctionParameter.select().where(
            FunctionParameter.function == function_id
        )
    ]

    return FunctionParameterOut(function=function, parameter=parameters)
