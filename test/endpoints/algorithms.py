import requests
from conftest import SERVICE_CONFIG

URL = f"{SERVICE_CONFIG.middleware}/algorithms/"


def get_algorithms_available():
    response = requests.get(URL)
    algorithms = response.json()["algorithms"]
    return {item.get("id"): item.get("name") for item in algorithms}
