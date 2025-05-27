from database.schema import FunctionParameter
from .checks.features import handle_feature_creation
from .checks.files import handle_user_file
from .validation_schema import (
    ModelOutput,
    FunctionData,
    GeneratorDataOutput,
)


def check_function_parameters(functions: list[FunctionData]) -> list[FunctionData]:
    """
    Validates function parameters by checking if all input parameters match those in the database.

    :param functions: List of function dictionaries containing function_id and parameters.
    :return: List of valid function IDs if all parameters match, otherwise an empty list.
    """
    function_data = []
    for function in functions:
        parameter_ids = FunctionParameter.select(FunctionParameter.parameter).where(
            FunctionParameter.function == function.get("function_id")
        )
        parameter_ids_list = [p.parameter_id for p in parameter_ids]
        input_param = [item["param_id"] for item in function.get("parameters")]
        # If the functions are passed they must have parameters
        if len(input_param) != len(parameter_ids_list):
            return []
        if all(p in parameter_ids_list for p in input_param):
            function_data.append(function)
            continue
        else:
            return []
    return function_data


def process_input(
    data: dict, function_data: list[FunctionData] | None, model: ModelOutput
) -> (GeneratorDataOutput, str):
    """
    Handle the input data based on whether it's a user file or feature creation.

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :param model: the chosen AI model
    :return: the GeneratorDataOutput object or an error message
    """
    if data.get("user_file") is not None:
        return handle_user_file(data, function_data, model)
    else:
        return handle_feature_creation(data, function_data, model)
