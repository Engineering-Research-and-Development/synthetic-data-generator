from pydantic import BaseModel

from database.validation_schema import Function, Parameter


class FunctionParameterOut(BaseModel):
    function: Function
    parameter: list[Parameter]
