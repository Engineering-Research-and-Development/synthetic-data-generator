import peewee

from database.schema import FunctionParameter, SystemModel, TrainedModel, ModelVersion
from routers.sdg_input.schema import DatasetOutput, SupportedDatatypes, ModelOutput


def check_functions(functions: list[dict]):
    for function in functions:
        parameter_ids = (FunctionParameter
                         .select(FunctionParameter.parameter)
                         .where(FunctionParameter.function == function.get('function_id')))
        parameter_ids_list = [p.parameter_id for p in parameter_ids]
        input_param = [item['param_id'] for item in function.get('parameters')]
        return all(p in parameter_ids_list for p in input_param)

def check_new_model(new_model: int, new_model_name: str):
    try:
        model = SystemModel.get_by_id(new_model)
    except peewee.DoesNotExist:
        return {}
    return ModelOutput(algorithm_name=model.name, model_name=new_model_name)

def check_selected_model(selected_model: int, version: str):
    try:
        model = TrainedModel.get_by_id(selected_model)
    except peewee.DoesNotExist:
        return False

    try:
        _ = ModelVersion.select().where(ModelVersion.trained_model==model.id and ModelVersion.version_name==version)
    except peewee.DoesNotExist:
        return False
    return True


def check_user_file(user_file: dict):
    dataset_outputs = []

    if not user_file:
        return dataset_outputs

    # Transpose user_file to a column-wise structure
    columns = {key: [entry[key] for entry in user_file] for key in user_file[0].keys()}

    for column_name, values in columns.items():
        if all(isinstance(v, (int, float)) for v in values):  # Check if numerical
            column_type = "numerical"
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


def check_features_created(features_created: dict):
    pass