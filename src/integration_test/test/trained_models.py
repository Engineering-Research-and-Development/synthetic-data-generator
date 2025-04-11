import time
import requests

from conftest import middleware

url = middleware + "/trained_models/"


def check_pushed_models():
    time.sleep(60)
    response = requests.get(url)
    json_response = response.json()
    assert len(json_response["models"]) >= 1
