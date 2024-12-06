"""This module contains utils functions used by the server for enforcing Pydantic models in input and
output validation can be enforced. Also since we are using an ORM to define database logic a conversion step is needed,
which is carried out in this section."""

from pydantic import BaseModel, ConfigDict,TypeAdapter
from typing import Literal

from model_registry.database.model import Algorithm


class ValidHeaders(BaseModel):
    x_client_type: Literal["frontend","generator","input_coherence"]


class AlgorithmOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

# TODO: Add further input validation to the model params with regex
class MlModelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    status: str
    version: int
    image: str
    input_shape: str
    dtype: str
    algorithm: AlgorithmOut


class ParameterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    param_name: str
    param_description: str
    dtype: str

class ModelParameterOut(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
    model:  MlModelOut
    parameter: ParameterOut
    parameter_value: float
    max_threshold: float
    min_threshold: float



class AlgorithmIn(BaseModel):
    name: str


class MlModelIn(BaseModel):
    image: str
    name: str
    status: str = 'Blank'
    description: str
    version: int = 0
    input_shape: str
    dtype: str
    algorithm: int | AlgorithmIn


class ParameterIn(BaseModel):
    param_name: str
    param_description: str
    dtype: str

class ModelParameterIn(BaseModel):
    model:  int
    parameter: int
    parameter_value: float
    max_threshold: float
    min_threshold: float

# In this way a client needs only to send the param/params he wants to modify and doesn't need to send the whole
# objects
class ModifyMlModel(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str  | None = None
    version: int | None = None
    image: str | None = None
    input_shape: str | None = None
    dtype: str | None = None
    algorithm: int | None = None

class ModifyParameter(BaseModel):
    param_name: str | None = None
    param_description: str | None = None
    dtype: str | None = None

class ModifyModelParameter(BaseModel):
    model:  int | None = None
    parameter: int | None = None
    parameter_value: float | None = None
    max_threshold: float | None = None
    min_threshold: float | None = None

