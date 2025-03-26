from typing import List
from pydantic import BaseModel, PositiveInt
from database.validation_schema import Algorithm, DataType


class AlgorithmList(BaseModel):
    algorithms: List[Algorithm]

class AlgorithmDatatype(BaseModel):
    algorithm: Algorithm
    datatypes: List[DataType]


