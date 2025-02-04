import peewee

from database.schema import FunctionParameter, Algorithm, TrainedModel, ModelVersion
from routers.sdg_input.schema import DatasetOutput, SupportedDatatypes, ModelOutput


def check_function_parameters(functions: list[dict]):
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


def check_new_model(new_model: int, model_name: str):
    try:
        algorithm = Algorithm.get(Algorithm.id == new_model)
        return ModelOutput(algorithm_name=algorithm.name, model_name=model_name)
    except peewee.DoesNotExist:
        return {}


def check_existing_model(selected_model: int, version: str):
    try:
        trained_model = TrainedModel.get_by_id(selected_model)
    except peewee.DoesNotExist:
        return {}

    try:
        model_version = ModelVersion.get(ModelVersion.trained_model==trained_model.id and ModelVersion.version_name==version)
    except peewee.DoesNotExist:
        return {}

    algorithm = Algorithm.get(Algorithm.id == trained_model.algorithm_id)
    return ModelOutput(algorithm_name=algorithm.name, model_name=trained_model.name,
                       input_shape=trained_model.input_shape, image=model_version.image_path)


def check_ai_model(data: dict):
    new_model = data.get('new_model', False)
    if new_model:
        model = check_new_model(data['selected_model'], data["new_model_name"])
    else:
        model = check_existing_model(data['selected_model'], data["model_version"])

    if model == {}:
        return {}
    return model


def determine_column_type(values: list) -> str:
    return "numerical" if all(isinstance(v, (int, float)) for v in values) else "categorical"


def check_user_file(user_file: list[dict]) -> list[DatasetOutput]:
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
