"""This module contains the definition of the database schema of our application """
from datetime import datetime


from sqlmodel import Field, SQLModel, Relationship
from model_registry.server.validation import BaseSystemModel, BaseModelVersion, BaseTrainedModel, BaseTrainingInfo, BaseFeatureSchema


class SystemModel(BaseSystemModel,table=True):
    pass

class TrainedModel(BaseTrainedModel,table=True):
    id: int | None = Field(default=None,primary_key=True)

class ModelVersion(BaseModelVersion,table=True):
    id: int | None = Field(default=None,primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False)
    trained_model_id: int | None = Field(default=None,foreign_key="trainedmodel.id",ondelete="CASCADE")
    training_info_id: int | None = Field(default=None,foreign_key="traininginfo.id")


# Represents the N-N relationship called in the diagram "Is Trained On".
# Keeps track of how the features are passed in input as well as their data types.
class FeatureSchema(BaseFeatureSchema,table=True):
    trained_model_id: int | None = Field(default=None,foreign_key="trainedmodel.id",primary_key=True)
    datatype_id: int | None = Field(default=None,foreign_key="datatype.id")

class TrainingInfo(BaseTrainingInfo,table=True):
    id: int | None = Field(default=None, primary_key=True)

# Note: Defines the data type that our registry accepts
class DataType(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: str = Field(unique=True)
    is_categorical: bool

# Represents the N-N relationship called in the diagram "Allows" that models what kind of data a model template allows
class AllowedDataType(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    algorithm_name: str = Field(foreign_key="systemmodel.name")
    datatype: int | None = Field(default=None,foreign_key="datatype.id")



tables = [SystemModel,TrainedModel,DataType,AllowedDataType,FeatureSchema,TrainingInfo,ModelVersion]