from typing import List
from pydantic import BaseModel, PositiveInt
from server.database.validation_schema import Algorithm, DataType


class AlgorithmList(BaseModel):
    algorithms: List[Algorithm]

class AlgorithmDatatype(BaseModel):
    algorithm: Algorithm
    datatype: List[DataType]

class AlgorithmDelete(BaseModel):
    algorithm_id: PositiveInt

