from database.schema import FunctionParameter


def check_functions(functions: list[dict]):
    for function in functions:
        parameter_ids = (FunctionParameter
                         .select(FunctionParameter.parameter)
                         .where(FunctionParameter.function == function.get('function_id')))
        parameter_ids_list = [p.parameter_id for p in parameter_ids]
        input_param = [item['param_id'] for item in function.get('parameters')]
        return all(p in parameter_ids_list for p in input_param)


def check_selected_model(selected_model):
    pass

def check_user_file(user_file):
    pass

def check_selected_version(selected_version):
    pass

def check_features_created(features_created):
    pass