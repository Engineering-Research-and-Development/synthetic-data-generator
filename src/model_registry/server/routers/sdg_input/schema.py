from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, PositiveInt


class ParametersInput(BaseModel):
    param_id: int
    value: float

class FunctionData(BaseModel):
    feature: str
    function_id: int
    parameters: List[ParametersInput]

class AiModel(BaseModel):
    selected_model_id: Optional[int]
    new_model: Optional[bool] = False
    new_model_name: Optional[str] = None
    model_version: Optional[str] = None

class UserDataInput(BaseModel):
    additional_rows: PositiveInt
    functions: List[FunctionData]
    ai_model: AiModel
    user_file: Optional[List[Dict]] = None
    features_created: Optional[List] = None

    @classmethod
    def validate_either_present(cls, v, values, field):
        if field.name == "user_file":
            if v is None and not values.get("features_created"):
                raise ValueError("Either 'user_file' or 'features_created' must be provided.")
        elif field.name == "features_created":
            if v is None and not values.get("user_file"):
                raise ValueError("Either 'user_file' or 'features_created' must be provided.")
        return v


class ModelOutput(BaseModel):
    algorithm_name: str
    model_name: Optional[str]
    input_shape: Optional[str] = None
    image: Optional[str] = None

class SupportedDatatypes(str, Enum):
    float = "float"
    int = "int"

class DatasetOutput(BaseModel):
    column_data: List[float | int]
    column_name: str
    column_type: str
    column_datatype: SupportedDatatypes

class GeneratorDataOutput(BaseModel):
    function_ids: List[PositiveInt]
    model: ModelOutput
    n_rows: PositiveInt
    dataset: List[DatasetOutput]