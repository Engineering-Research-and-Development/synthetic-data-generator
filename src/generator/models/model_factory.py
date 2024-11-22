from utils.model_utils import parse_stringed_input_shape
from models.Model import Model
from traceback import print_tb

def get_model(model: dict) -> Model:
    try:
        model_file = model.get("image", "")
        metadata = model.get("metadata", {})
        input_shape = parse_stringed_input_shape(metadata.get("input_shape", ""))
        module_name = metadata.get("algorithm", "")

        if model_file != "":
            model = Model.from_image(model_file)
        else:
            print(input_shape)
            model = Model.from_module(module_name, input_shape)
        return model
    except ValueError as e:
        print_tb(e.__traceback__)
        print("Data is missing from request", e)




if __name__ == "__main__":

    test = {
        "model_file": "",
        "metadata": {
            "algorithm": "KerasTabularVAE",
            "input_shape": "(10)"
        }
    }
    m = get_model(test)
    print(m)