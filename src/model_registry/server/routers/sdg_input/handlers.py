from typing import Dict

import peewee

from src.model_registry.server.database.schema import FunctionParameter, Algorithm, TrainedModel, ModelVersion
from src.model_registry.server.routers.sdg_input.schema import DatasetOutput, SupportedDatatypes, ModelOutput

def check_function_parameters(functions: list[dict]) -> list:
    """
    Validates function parameters by checking if all input parameters match those in the database.

    :param functions: List of function dictionaries containing function_id and parameters.
    :return: List of valid function IDs if all parameters match, otherwise an empty list.
    """
    functions_id = []
    for function in functions:
        parameter_ids = (FunctionParameter
                         .select(FunctionParameter.parameter)
                         .where(FunctionParameter.function == function.get('function_id')))
        parameter_ids_list = [p.parameter_id for p in parameter_ids]
        input_param = [item['param_id'] for item in function.get('parameters')]
        if all(p in parameter_ids_list for p in input_param):
            functions_id.append(function['function_id'])
            continue
        else:
            return []
    return functions_id


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


def check_existing_model(selected_model: int, version: str) -> ModelOutput | Dict:
    """
    Checks if an existing trained model and its version exist in the database.

    :param selected_model: ID of the trained model.
    :param version: Version name of the model.
    :return: ModelOutput object with model details, or an empty dictionary if not found.
    """
    try:
        trained_model = TrainedModel.get_by_id(selected_model)
    except peewee.DoesNotExist:
        return {}

    try:
        model_version = ModelVersion.get(ModelVersion.trained_model == trained_model.id and ModelVersion.version_name == version)
    except peewee.DoesNotExist:
        return {}

    algorithm = Algorithm.get(Algorithm.id == trained_model.algorithm_id)
    return ModelOutput(algorithm_name=algorithm.name, model_name=trained_model.name,
                       input_shape=trained_model.input_shape, image=model_version.image_path)


def check_ai_model(data: dict) -> ModelOutput | Dict:
    """
    Determines whether to check for a new or existing AI model and retrieves its details.

    :param data: Dictionary containing AI model selection details.
    :return: ModelOutput object or an empty dictionary if the model is not found.
    """
    new_model = data.get('new_model', False)
    if new_model:
        model_output = check_new_model(data['selected_model'], data["new_model_name"])
    else:
        model_output = check_existing_model(data['selected_model'], data["model_version"])

    if model_output == {}:
        return {}
    return model_output


def determine_column_type(values: list) -> str:
    """
    Determines whether a column contains numerical or categorical data.

    :param values: List of values in the column.
    :return: "numerical" if all values are integers or floats, otherwise "categorical".
    """
    return "numerical" if all(isinstance(v, (int, float)) for v in values) else "categorical"


def check_user_file(user_file: list[dict]) -> list[DatasetOutput]:
    """
    Processes a user-provided file to analyze column types and data formats.

    :param user_file: List of dictionaries representing user-provided data.
    :return: List of DatasetOutput objects describing the processed dataset.
    """
    dataset_outputs = []

    if not user_file:
        return dataset_outputs

    # Transpose user_file to a column-wise structure
    columns = {key: [entry[key] for entry in user_file] for key in user_file[0].keys()}

    for column_name, values in columns.items():
        column_type = determine_column_type(values)

        if column_type == "numerical":
            column_datatype = SupportedDatatypes.int if all(isinstance(v, int) for v in values) else SupportedDatatypes.float
            dataset_outputs.append(
                DatasetOutput(
                    column_data=values,
                    column_name=column_name,
                    column_type=column_type,
                    column_datatype=column_datatype
                )
            )

    return dataset_outputs
