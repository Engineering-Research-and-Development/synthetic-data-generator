from models.classes.Model import UnspecializedModel
from traceback import print_tb

import importlib
import pandas as pd


def dynamic_import(class_name:str):
    module_name, class_name = class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def model_factory(request: dict) -> UnspecializedModel:
    try:
        model_file = request.get("image", None)
        metadata = request.get("metadata", {})
        model_type = request.get("algorithm", "")

        ModelClass = dynamic_import(model_type)
        model = ModelClass(metadata, model_type, model_file)
        model.initialize()
        return model

    except ValueError as e:
        print_tb(e.__traceback__)
        print("Data is missing from request", e)



if __name__ == "__main__":

    test = {
        "model_file": "",
        "algorithm": "models.classes.keras.keras_tabular_vae.KerasTabularVAE",
        "metadata": {
            "input_shape": "(13)"
        }
    }
    m = model_factory(test)
    csv = pd.read_csv("wine_clean.csv")
    data = csv.values
    m.train(data)
    print(m)
    print(m.metadata)