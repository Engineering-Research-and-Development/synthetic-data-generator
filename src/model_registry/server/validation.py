"""This module defines a series of pydantic's model for input and output santitization/validation."""

from sqlmodel import Field,SQLModel
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class ValidHeaders(BaseModel):
    x_client_type: Literal["frontend", "generator", "input_coherence"]


class BaseSystemModel(SQLModel):
    name: str = Field(primary_key=True)
    description: str
    loss_function: str

class CreateSystemModel(BaseSystemModel):
    pass


class BaseModelVersion(SQLModel):
    version_name: str
    model_image_path: str

class CreateModelVersion(BaseModelVersion):
    pass


class BaseTrainedModel(SQLModel):
    name: str
    dataset_name: str
    size: str
    # Workaround in order to use regex validation of pydantic. See issue here: https://github.com/fastapi/sqlmodel/discussions/735
    # This regex matches any input that is in the form of (number,number,...,number). This first digit must not start
    # with zero.
    input_shape: str = Field(schema_extra={'pattern':r"^\([1-9]\d*(?:,[1-9]\d*)*\)$"})
    algorithm_name: str = Field(foreign_key="systemmodel.name",nullable=False)

class CreateTrainedModel(BaseTrainedModel):
    pass


class BaseTrainingInfo(SQLModel):
    loss_function: str
    train_loss_value: float
    val_loss_value: float
    n_train_samples: int
    n_validation_samples: int

class CreateTrainingInfo(BaseTrainingInfo):
    pass

class BaseFeatureSchema(SQLModel):
        feature_name: str
        feature_position: int = Field(primary_key=True)


class CreateFeatureSchema(BaseFeatureSchema):
    datatype: str