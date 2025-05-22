from typing import List
from pydantic import BaseModel, PositiveInt
from database.validation_schema import Function, Parameter


class FunctionParameterOut(BaseModel):
    function: Function
    parameter: List[Parameter]


class FunctionParameterIn(BaseModel):
    function: Function
    parameters: List[Parameter]


class FunctionID(BaseModel):
    id: PositiveInt
