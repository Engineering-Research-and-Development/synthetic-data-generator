from typing import Dict

import peewee
import ast
from database.schema import (
    FunctionParameter,
    Algorithm,
    TrainedModel,
    ModelVersion,
    Parameter,
)
from .validation_schema import (
    DatasetOutput,
    SupportedDatatypes,
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


def check_new_model(new_model: int, model_name: str) -> ModelOutput | Dict:
    """
    Checks if a new model exists in the Algorithm database and returns model details.

    :param new_model: Algorithm ID of the new model.
    :param model_name: Name of the model.
    :return: ModelOutput object with algorithm and model name, or an empty dictionary if not found.
    """
    try:
        algorithm = Algorithm.get(Algorithm.id == new_model)
        return ModelOutput(algorithm_name=algorithm.name, model_name=model_name)
    except peewee.DoesNotExist:
        return {}


def check_existing_model(selected_model_id: int, version: str) -> ModelOutput | Dict:
    """
    Checks if an existing trained model and its version exist in the database.

    :param selected_model_id: ID of the trained model.
    :param version: Version name of the model.
    :return: ModelOutput object with model details, or an empty dictionary if not found.
    """
    try:
        trained_model = TrainedModel.get_by_id(selected_model_id)
    except peewee.DoesNotExist:
        return {}

    try:
        model_version = ModelVersion.get(
            ModelVersion.trained_model == trained_model.id
            and ModelVersion.version_name == version
        )
    except peewee.DoesNotExist:
        return {}

    algorithm = Algorithm.get(Algorithm.id == trained_model.algorithm_id)
    return ModelOutput(
        algorithm_name=algorithm.name,
        model_name=trained_model.name,
        input_shape=trained_model.input_shape,
        image=model_version.image_path,
    )


def check_ai_model(data: dict) -> ModelOutput | Dict:
    """
    Determines whether to check for a new or existing AI model and retrieves its details.

    :param data: Dictionary containing AI model selection details.
    :return: ModelOutput object or an empty dictionary if the model is not found.
    """
    new_model = data.get("new_model", False)
    if new_model:
        model_output = check_new_model(
            data["selected_model_id"], data["new_model_name"]
        )
    else:
        model_output = check_existing_model(
            data["selected_model_id"], data["model_version"]
        )

    if model_output == {}:
        return {}
    return model_output


def determine_column_type(values: list) -> str:
    """
    Determines whether a column contains continuous or categorical data.

    :param values: List of values in the column.
    :return: "continuous" if all values are integers or floats, otherwise "categorical".
    """
    if isinstance(values[0], list):
        return "time_series"
    else:
        return "continuous"


def determine_column_datatype(values: list) -> SupportedDatatypes:
    if isinstance(values[0], list):
        return determine_column_datatype(values[0])
    else:
        return (
            SupportedDatatypes.int
            if all(isinstance(v, int) for v in values)
            else SupportedDatatypes.float.value
        )


def check_user_file(user_file: list[dict]) -> list[DatasetOutput]:
    """
    Processes a user-provided file to analyze column types and data formats.

    :param user_file: List of dictionaries representing user-provided data.
    :return: List of DatasetOutput objects describing the processed dataset.
    """
    dataset_outputs = []

    # Transpose user_file to a column-wise structure
    columns = {
        key: [ast.literal_eval(str(entry[key])) for entry in user_file]
        for key in user_file[0].keys()
        if key != ""
    }

    for column_name, values in columns.items():
        column_type = determine_column_type(values)
        column_datatype = determine_column_datatype(values)
        dataset_outputs.append(
            DatasetOutput(
                column_data=values,
                column_name=column_name,
                column_type=column_type,
                column_datatype=column_datatype,
            )
        )

    return dataset_outputs


def check_features_created_types(features: list[dict], function_ids: list[int]):
    """
    This function checks if the features that the user has created and passed in input are
    consistent with the functions' parameters tha have been selected
    :return:
    """
    functions_param_types = (
        Parameter.select()
        .join(FunctionParameter)
        .where(FunctionParameter.function << function_ids)
    )

    function_params_dict = {
        elem["parameter_type"]: "" for elem in functions_param_types.dicts()
    }
    for feature in features:
        if function_params_dict.get(feature["type"]) is None:
            return False, feature["type"]
    return True, None


def handle_user_file(
    data: dict, function_data: list[FunctionData] | None, model
) -> (GeneratorDataOutput, str):
    """
    Create the GeneratorDataOutput object from the user file

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :param model: the chosen AI model
    :return: the GeneratorDataOutput object or an error message
    """
    user_file = check_user_file(data.get("user_file"))
    if not user_file:
        return None, "Error parsing input dataset"

    return (
        GeneratorDataOutput(
            functions_id=function_data,
            n_rows=data.get("additional_rows"),
            model=model,
            dataset=user_file,
        ),
        "",
    )


def handle_feature_creation(
    data: dict, function_data: list[FunctionData] | None, model
) -> (GeneratorDataOutput, str):
    """
    Create the GeneratorDataOutput object from the list of features

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :param model: the chosen AI model
    :return: the GeneratorDataOutput object or an error message
    """
    result, error = check_features_created_types(
        data.get("features_created"), data["functions"]
    )

    if not result:
        return (
            None,
            f"The functions chosen are not compatible with the following feature that you want to create ({error})",
        )

    return (
        GeneratorDataOutput(
            functions_id=function_data,
            n_rows=data.get("additional_rows"),
            model=model,
        ),
        "",
    )


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
