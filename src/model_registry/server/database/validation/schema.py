"""This module defines a series of pydantic's model for input and output santitization/validation."""
from typing import Literal, Annotated

from pydantic import BaseModel, BeforeValidator, Field


class CreateAlgorithm(BaseModel):
    name: str
    description: str
    default_loss_function: str


class Algorithm(CreateAlgorithm):
    id: int

class DataType(BaseModel):
    id: int
    type: str
    is_categorical : bool

class CreateDataType(BaseModel):
    type: str
    is_categorical : bool

class AllowedDataType(BaseModel):
    id : int
    algorithm_name : str
    data_type : str

class CreateAllowedData(BaseModel):
    datatype: str
    is_categorical: bool

class AlgorithmAndAllowedDatatypes(Algorithm):
    allowed_data: list[CreateAllowedData] | None


class CreateTrainedModel(BaseModel):
    name: str
    dataset_name: str
    size: str
    input_shape: str
    algorithm_id: int

class TrainedModel(CreateTrainedModel):
    id : int
    algorithm_name: str

def convert_to_list(value: int) -> list:
    if type(value) is int:
        return [value]
    else:
        return [int(x) for x in value.split(',')]

class TrainedModelAndVersionIds(TrainedModel):
    version_ids: Annotated[list[int], BeforeValidator(convert_to_list)] | None

class Features(BaseModel):
    id : int
    feature_name : str
    datatype : int
    feature_position : int
    trained_model : int

# This is the features that we get in input and we delegate to job to find the ids to the model registry
class CreateFeatures(BaseModel):
    feature_name: str
    feature_position : int
    is_categorical: bool
    datatype: str

class TrainedModelAndFeatureSchema(TrainedModel):
    feature_schema: list[CreateFeatures] | None = None

class CreateTrainingInfo(BaseModel):
    loss_function : str
    train_loss : float
    val_loss : float
    train_samples : int
    val_samples : int

class TrainingInfo(CreateTrainingInfo):
    id : int

class CreateModelVersion(BaseModel):
    version_name : str
    image_path : str


class ModelVersion(CreateModelVersion):
    id : int


class ModelVersionAndTrainInfo(BaseModel):
    version: ModelVersion
    training_info: TrainingInfo


class TrainedModelAndVersions(TrainedModel):
    versions: list[ModelVersionAndTrainInfo] | None = Field(description="This is a list of the trained model"
                                                            " versions and training infos")
    feature_schema: list[CreateFeatures] | None = Field(description="This is a list of the features that the trained model"
                                                            " has")
class AlgorithmsAndTrainedModels(BaseModel):
    algorithms: list[AlgorithmAndAllowedDatatypes]
    trained_models: list[TrainedModelAndVersionIds]

## BEHAVIOUR MODELS

class Function(BaseModel):
    id: int
    name: str
    description: str
    function_reference: str

class Parameter(BaseModel):
    id: int
    name: str
    value: str
    parameter_type: Literal['float']

class FunctionParameter(BaseModel):
    function: int
    parameter: int

class FunctionParameterOut(BaseModel):
    function: Function
    parameter: list[Parameter]