from typing import List, Optional
from pydantic import BaseModel, PositiveInt

class ParametersInput(BaseModel):
    param_id: int
    value: float

class FunctionData(BaseModel):
    feature: str
    function_id: int
    parameters: List[ParametersInput]

class UserFileEntry(BaseModel):
    Name: str
    Age: int  # Changed from str to int
    Occupation: str
    Salary: int  # Changed from str to int

class UserDataInput(BaseModel):
    additional_rows: PositiveInt
    functions: List[FunctionData]
    selected_model: int
    user_file: Optional[List[UserFileEntry]] = None
    new_model: Optional[bool] = None
    selected_version: Optional[int] = None
    features_created: Optional[List] = None
