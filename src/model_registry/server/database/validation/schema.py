"""This module defines a series of pydantic's model for input and output santitization/validation."""
from datetime import datetime

from pydantic import BaseModel, Field

from pydantic.v1 import validator

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

class TrainedModel(BaseModel):
    id : int
    name : str
    dataset_name : str
    size : str
    input_shape : str
    algorithm_name :str

class Features(BaseModel):
    id : int
    feature_name : str
    datatype : str
    feature_position : int
    trained_model : str

class TrainingInfo(BaseModel):
    id : int
    loss_function : str
    train_loss_value : float
    val_loss_value : float
    n_train_sample : int
    n_validation_sample : int

class ModelVersion(BaseModel):
    id : int
    version_name : str
    model_image_path : str
    timestamp : datetime
    trained_model : str
    training_info : str
