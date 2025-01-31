"""This module defines a series of pydantic's model for input and output santitization/validation."""
from datetime import datetime
from typing import Literal,Annotated

from pydantic import BaseModel,BeforeValidator,Field
from pydantic.dataclasses import dataclass


class SystemModel(BaseModel):
    name: str
    description: str
    loss_function: str

class DataType(BaseModel):
    id: int
    type: str
    is_categorical : bool

class AllowedDataType(BaseModel):
    id : int
    algorithm_name : str
    datatype : str

class CreateTrainedModel(BaseModel):
    name: str
    dataset_name: str
    size: str
    input_shape: str
    algorithm_id: int

class TrainedModel(CreateTrainedModel):
    id : int


def convert_to_list(value: int) -> list:
    if type(value) is int:
        return [value]
    else:
        return [int(x) for x in value.split(',')]

class TrainedModelAndVersionIds(TrainedModel):
    version_ids: Annotated[list[int], BeforeValidator(convert_to_list)] | None

class CreateFeatures(BaseModel):
    feature_name : str
    datatype : str
    feature_position : int
    trained_model : str

class Features(CreateFeatures):
    id : int

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
    model_image_path : str
    timestamp : datetime
    trained_model : int
    training_info : int

class ModelVersion(CreateModelVersion):
    id : int


class ModelVersionAndTrainInfo(BaseModel):
    version: ModelVersion
    training_info: TrainingInfo


class TrainedModelAndVersions(TrainedModel):
    versions: list[ModelVersionAndTrainInfo] | None = Field(description="This is a list of the trained model"
                                                            " versions and training infos")


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