from pydantic import BaseModel, PositiveInt, Field
from typing import List, Literal


class DatasetIn(BaseModel):
    column_data: List[float | int] | List
    column_name: str
    column_datatype: Literal["float32", "float64", "int32", "int64"]
    column_type: Literal["continuous", "categorical", "time_series"]


class TrainModelInfo(BaseModel):
    algorithm_name: str
    model_name: str


class TrainRequest(BaseModel):
    model : TrainModelInfo
    dataset : List[DatasetIn]
    functions_id : list[PositiveInt]
    n_rows : PositiveInt



class TrainingDataInfo(BaseModel):
    column_name: str
    column_datatype: Literal["float32", "float64", "int32", "int64"]
    column_type: Literal["continuous", "categorical", "time_series"]


class InferModelInfoNodata(BaseModel):
    algorithm_name: str
    model_name: str
    image: str
    input_shape: str = Field(pattern=r"\([0-9]+,(([0-9]+,?)+)?\)")
    training_data_info: List[TrainingDataInfo]


class InferModelInfoData(BaseModel):
    algorithm_name: str
    model_name: str
    image: str
    input_shape: str = Field(pattern=r"\([0-9]+,(([0-9]+,?)+)?\)")



class InferRequestData(BaseModel):
    model : InferModelInfoData
    dataset : List[DatasetIn]
    functions_id : list[PositiveInt]
    n_rows : PositiveInt


class InferRequestNoData(BaseModel):
    model : InferModelInfoNodata
    functions_id : list[PositiveInt]
    n_rows : PositiveInt

