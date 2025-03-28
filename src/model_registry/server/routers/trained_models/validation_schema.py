from typing import List
from pydantic import BaseModel, PositiveInt
from database.validation_schema import (
    TrainedModel,
    ModelVersion,
    TrainModelDatatype,
    DataType,
)


class ModelVersionPublic(ModelVersion):
    trained_model: PositiveInt


class TrainedModelPublic(TrainedModel):
    algorithm: PositiveInt


class TrainedModelVersion(BaseModel):
    model: TrainedModelPublic
    versions: List[ModelVersionPublic]


class TrainedModelVersionList(BaseModel):
    models: List[TrainedModelVersion]


class MergedDataType(TrainModelDatatype, DataType):
    pass


class TrainedModelVersionDatatype(TrainedModelVersion):
    datatypes: List[MergedDataType]


class PostTrainedModelVersionDatatype(BaseModel):
    model: TrainedModelPublic
    version: ModelVersion
    datatypes: List[MergedDataType]


class PostTrainedModelOut(BaseModel):
    trained_model_id: PositiveInt
    model_version_id: PositiveInt


class TrainedModelDelete(BaseModel):
    model_id: PositiveInt


class TrainedModelVersionDelete(TrainedModelDelete):
    version_id: PositiveInt
