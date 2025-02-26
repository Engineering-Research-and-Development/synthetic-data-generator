from pydantic import BaseModel, PositiveInt, Field
from typing import List, Literal


class GeneratedData(BaseModel):
    column_data: List[float | int]
    column_name: str
    column_datatype: Literal["float32", "float64", "int32", "int64"]
    column_type: Literal["continuous", "categorical"]


class Response(BaseModel):
    result_data: GeneratedData
    metrics: dict
