import requests
from conftest import middleware

url = middleware + "/algorithms/"


def get_algorithms_available():
    response = requests.get(url)
    algorithms = response.json()["algorithms"]
    return {item.get("id"): item.get("name") for item in algorithms}
