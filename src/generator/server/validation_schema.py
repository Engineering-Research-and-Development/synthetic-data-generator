from pydantic import BaseModel, PositiveInt, Field
from typing import List, Literal

class TrainingDataInfo(BaseModel):
    column_name: str
    column_datatype: Literal["float32", "float64", "int32", "int64"]
    column_type: Literal["continuous", "categorical", "time_series"]


class DatasetIn(TrainingDataInfo):
    column_data: List[float | int] | List


class TrainModelInfo(BaseModel):
    algorithm_name: str
    model_name: str


class TrainRequest(BaseModel):
    model : TrainModelInfo
    dataset : List[DatasetIn]
    functions_id : list[PositiveInt]
    n_rows : PositiveInt

class InferModelInfoData(BaseModel):
    algorithm_name: str
    model_name: str
    image: str
    input_shape: str = Field(pattern=r"\([0-9]+,(([0-9]+,?)+)?\)")


class InferModelInfoNodata(InferModelInfoData):
    training_data_info: List[TrainingDataInfo]


class InferRequestNoData(BaseModel):
    model : InferModelInfoNodata
    functions_id : list[PositiveInt]
    n_rows : PositiveInt


class InferRequestData(InferRequestNoData):
    dataset : List[DatasetIn]


##################################
class GeneratedData(BaseModel):
    column_data: List[float | int]
    column_name: str
    column_datatype: Literal["float32", "float64", "int32", "int64"]
    column_type: Literal["continuous", "categorical"]


class GeneratedResponse(BaseModel):
    result_data: GeneratedData
    metrics: dict

class CouchEntry(BaseModel):
    doc_id: str