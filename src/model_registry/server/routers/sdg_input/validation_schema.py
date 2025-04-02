from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, PositiveInt, model_validator, Field


class ParametersInput(BaseModel):
    param_id: PositiveInt
    value: float


class FunctionData(BaseModel):
    feature: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A feature name"],
    )
    function_id: PositiveInt
    parameters: List[ParametersInput]


class AiModel(BaseModel):
    selected_model_id: PositiveInt
    new_model: Optional[bool] = False
    new_model_name: Optional[str] = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="The name of the new AI model.\n"
        "This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A name of a new model"],
        default=None
    )
    model_version: Optional[str] = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="The name of the version of the AI model.\n"
        "This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a version"],
        default=None
    )


class SupportedDatatypes(str, Enum):
    float = "float32"
    int = "int32"


class SupportedDatatypesCategory(str, Enum):
    continuous = "continuous"
    categorical = "categorical"


class FeaturesCreated(BaseModel):
    feature: str
    type: SupportedDatatypes
    category: SupportedDatatypesCategory

    class Config:
        use_enum_values = True


class UserDataInput(BaseModel):
    additional_rows: PositiveInt
    functions: Optional[List[FunctionData]] = []
    ai_model: AiModel
    user_file: Optional[List[Dict]] = None
    features_created: Optional[List[FeaturesCreated]] = None

    @model_validator(mode="after")
    def validate_either_present(self):
        if (self.user_file is None) != (self.features_created is None):
            return self
        else:
            raise ValueError(
                "Either 'user_file' or 'features_created' must be provided. Not both"
            )


class ModelOutput(BaseModel):
    algorithm_name: str
    model_name: Optional[str]
    input_shape: Optional[str] = None
    image: Optional[str] = None


class DatasetOutput(BaseModel):
    column_data: List[float | int]
    column_name: str
    column_type: str
    column_datatype: SupportedDatatypes

    class Config:
        use_enum_values = True


class GeneratorDataOutput(BaseModel):
    functions_id: List[PositiveInt]
    model: ModelOutput
    n_rows: PositiveInt
    dataset: List[DatasetOutput] | None = None
