"""This module defines a series of pydantic's model for input and output santitization/validation."""

from typing import Literal, Annotated

from pydantic import BaseModel, BeforeValidator, Field, PositiveInt


class CreateAlgorithm(BaseModel):
    name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A name of an algorithm"],
    )
    description: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A description of an algorithm"],
    )
    default_loss_function: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a loss function"],
    )


class Algorithm(CreateAlgorithm):
    id: PositiveInt


class DataType(BaseModel):
    id: PositiveInt
    type: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The type of a datatype"],
    )
    is_categorical: bool


class CreateDataType(BaseModel):
    datatype: str
    is_categorical: bool


class AlgorithmDataType(BaseModel):
    id: PositiveInt
    algorithm_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of analgorithm"],
    )
    data_type: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The data type"],
    )


class CreateAllowedData(BaseModel):
    datatype: str
    is_categorical: bool


class AlgorithmAndAllowedDatatypes(Algorithm):
    allowed_data: list[CreateAllowedData] | None


class CreateTrainedModel(BaseModel):
    name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a trained model"],
    )
    dataset_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a dataset"],
    )
    size: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The size of a dataset"],
    )
    input_shape: str = Field(
        pattern=r"\([0-9]+,(([0-9]+,?)+)?\)",
        description="The shape of the input that must be in the format of (number,...,number)",
        examples=["(1,3,200,200)"],
    )
    algorithm_id: PositiveInt


class TrainedModel(CreateTrainedModel):
    id: PositiveInt
    algorithm_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of the algorithm"],
    )


def convert_to_list(value: int | str) -> list:
    if type(value) is int:
        return [value]
    else:
        return [int(x) for x in value.split(",")]


class TrainedModelAndVersionIds(TrainedModel):
    version_ids: Annotated[list[PositiveInt], BeforeValidator(convert_to_list)] | None


class Features(BaseModel):
    id: PositiveInt
    feature_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a feature"],
    )
    datatype: PositiveInt
    feature_position: int
    trained_model: PositiveInt


# This is the features that we get in input and we delegate to job to find the ids to the model registry
class CreateFeatures(BaseModel):
    feature_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a feature"],
    )
    feature_position: int
    is_categorical: bool
    datatype: str


class TrainedModelAndFeatureSchema(TrainedModel):
    feature_schema: list[CreateFeatures] | None = None


class CreateTrainingInfo(BaseModel):
    loss_function: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A loss function"],
    )
    train_loss: float
    val_loss: float
    train_samples: int
    val_samples: int


class TrainingInfo(CreateTrainingInfo):
    id: PositiveInt
    model_version_id: int


class CreateModelVersion(BaseModel):
    version_name: str
    image_path: str


class ModelVersion(CreateModelVersion):
    id: PositiveInt


class ModelVersionAndTrainInfo(BaseModel):
    version: ModelVersion
    training_info: TrainingInfo


class TrainedModelAndVersions(TrainedModel):
    versions: list[ModelVersionAndTrainInfo] | list[ModelVersion] | None = Field(
        description="This is a list of the trained model versions and training infos"
    )
    feature_schema: list[CreateFeatures] | None = Field(
        description="This is a list of the features that the trained model has"
    )


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
    parameter_type: Literal["float"]


class FunctionParameter(BaseModel):
    function: int
    parameter: int


class FunctionParameterOut(BaseModel):
    function: Function
    parameter: list[Parameter]
