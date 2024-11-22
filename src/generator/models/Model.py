import importlib
import pkgutil
from yaml import load
import pickle
from keras import saving
import yaml


config_path = "./models/config.yaml"
f = pkgutil.get_data("models", "config.yaml")
config = yaml.safe_load(f)


class Model:
    def __init__(self, model):
        self.model = model
        self.metadata = {}


    @classmethod
    def from_module(cls, module_name:str, input_shape:tuple[int, ...]):
        module_ = importlib.import_module(module_name)
        model = module_.create_model(input_shape)
        return cls(model)

    @classmethod
    def from_image(cls, file_img):

        model_formats = config["model_format"]
        key = None
        model = None

        for key, value in model_formats.items():
            if file_img.endswith(value):
                break

        try:
            if key == "sklearn":
                model = pickle.load(file_img)
            elif key == "keras":
                model = saving.load_model(file_img)

            return cls(model)
        except FileNotFoundError as e:
            print(e)

