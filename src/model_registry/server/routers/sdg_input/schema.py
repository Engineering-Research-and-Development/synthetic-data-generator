from enum import Enum
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, PositiveInt

class ParametersInput(BaseModel):
    param_id: int
    value: float

class FunctionData(BaseModel):
    feature: str
    function_id: int
    parameters: List[ParametersInput]

class UserDataInput(BaseModel):
    additional_rows: PositiveInt
    functions: List[FunctionData]
    selected_model: int
    user_file: Optional[List[Dict]] = None
    new_model: Optional[bool] = None
    new_model_name: Optional[str] = None
    model_version: Optional[str] = None
    features_created: Optional[List] = None


############################
class ModelOutput(BaseModel):
    algorithm_name: str
    model_name: str

class SupportedDatatypes(str, Enum):
    float = "float"
    int = "int"

class DatasetOutput(BaseModel):
    column_data: List[float | int]
    column_name: str
    column_type: str
    column_datatype: Literal[SupportedDatatypes.float, SupportedDatatypes.int]

class TrainingOutput(BaseModel):
    function_ids: List[PositiveInt]
    model: ModelOutput
    n_rows: PositiveInt
    dataset: List[DatasetOutput]