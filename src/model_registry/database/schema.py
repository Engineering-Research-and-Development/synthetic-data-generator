"""This module contains the definition of the database schema of our application """
from email.policy import default
from datetime import datetime
from sqlmodel import Field,SQLModel
from ..server.validation import BaseSystemModel, BaseModelVersion, BaseTrainedModel, BaseTrainingInfo, BaseFeatureSchema


class SystemModel(BaseSystemModel,table=True):
    pass


class TrainedModel(BaseTrainedModel,table=True):
    id: int | None = Field(default=None,primary_key=True)



# Note: Defines the data type that our registry accepts
class DataType(SQLModel,table=True):
    type: str = Field(unique=True,primary_key=True)

# Represents the N-N relationship called in the diagram "Allows" that models what kind of data a model template allows
class AllowedDataType(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    algorithm_name: str = Field(foreign_key="systemmodel.name")
    datatype: str = Field(foreign_key="datatype.type")

# Represents the N-N relationship called in the diagram "Is Trained On".
# Keeps track of how the features are passed in input as well as their data types.
class FeatureSchema(BaseFeatureSchema,table=True):
    trained_model_id: int | None = Field(default=None,foreign_key="trainedmodel.id",primary_key=True)

class TrainingInfo(BaseTrainingInfo,table=True):
    id: int | None = Field(default=None, primary_key=True)


class ModelVersion(BaseModelVersion,table=True):
    id: int | None = Field(default=None,primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False)
    trained_model_id: int | None = Field(foreign_key="trainedmodel.id")
    training_info_id: int | None = Field(foreign_key="traininginfo.id")



tables = [SystemModel,TrainedModel,DataType,AllowedDataType,FeatureSchema,TrainingInfo,ModelVersion]