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
    input_shape: str
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