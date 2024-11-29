import requests
from urllib3.exceptions import NewConnectionError
from yaml import safe_load
import pkgutil

config_file = pkgutil.get_data("services", "config.yaml")
config = safe_load(config_file)
model_registry = config["model_registry"]

def get_model_by_id(model_id: int) -> dict:

    try:
        api = model_registry["url"] + "get_model_by_id/" + str(model_id)
        response = requests.get(api)
        return response.json()
    except NewConnectionError as e:
        print(e)
