from exceptions.ModelException import ModelException
from models.classes.Model import UnspecializedModel
from traceback import print_tb
import importlib

from utils.parsing import parse_model_info


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
        "input_shape" [optional] -> contains a stringed tuple that identifies the input layer shape
    }
    :param input_shape:
    :return: An instance of a BaseModel class or any subclass
    :raises: ModelException
    """
    model_file, metadata, model_type, model_name, input_shape_model = parse_model_info(model_dict)
    if input_shape is None:
        input_shape = input_shape_model

    if model_type is None:
        raise ModelException(f"Model algorithm not provided")
    elif model_name is None:
        raise ModelException(f"Model name not provided")


    ModelClass = dynamic_import(model_type)
    model = ModelClass(metadata, model_name, model_file)
    model.initialize(input_shape)
    return model





