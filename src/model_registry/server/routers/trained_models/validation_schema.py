from typing import List

from pydantic import BaseModel, PositiveInt

from database.validation_schema import TrainedModel, ModelVersion, TrainModelDatatype


class TrainedModelVersion(BaseModel):
    model: TrainedModel
    version: List[ModelVersion]


class TrainedModelVersionList(BaseModel):
    models: List[TrainedModelVersion]


class TrainedModelVersionDatatype(TrainedModelVersion):
    datatype: List[TrainModelDatatype]


class TrainedModelDelete(BaseModel):
    model_id: PositiveInt


class TrainedModelVersionDelete(TrainedModelDelete):
    version_id: PositiveInt
