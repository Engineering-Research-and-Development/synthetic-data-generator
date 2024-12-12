from exceptions.ModelException import ModelException
from models.classes.Model import UnspecializedModel
from traceback import print_tb
import importlib



def dynamic_import(class_name:str):
    module_name, class_name = class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def model_factory(model_dict: dict, input_shape:str=None) -> UnspecializedModel:
    """
    This function is a generic model factory. Takes a dictionary containing useful model information and plugs
    them in the model itself.
    Input shape may be passed as an argument (i.e) from the request data itself, or [alternatively] may be present in
    model dictionary. If not explicitly passed, it will use the model dictionary

    :param model_dict: A dictionary containing model information, structured as follows:
    {
        "image" -> contains the possible path where to find the model image. If not none, model will be loaded from there
        "metadata" -> a dictionary itself, containing miscellaneous information
        "algorithm_name" -> includes the model class module to load
        "model_name" -> the model name, used to identify the model itself
        "input_shape" [optioal] -> contains a stringed tuple that identifies the input layer shape
    }
    :param input_shape:
    :return:
    """
    try:
        model_file = model_dict.get("image", None)
        metadata = model_dict.get("metadata", {})
        model_type = model_dict.get("algorithm_name", "")
        model_name = model_dict.get("model_name", "Foo")
        if input_shape is None:
            input_shape = model_dict.get("input_shape", "")

    except ValueError as e:
        raise ModelException(f"Model is missing useful information: {str(e)}")

    ModelClass = dynamic_import(model_type)
    model = ModelClass(metadata, model_name, model_file)
    model.initialize(input_shape)
    return model





