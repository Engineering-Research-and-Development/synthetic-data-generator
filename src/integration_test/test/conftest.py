import glob
import json
import os

middleware = os.environ.get("MIDDLEWARE", "http://127.0.0.1:8001")
generator = os.environ.get("GENERATOR", "http://127.0.0.1:8010")
couch = os.environ.get("COUCH", "http://127.0.0.1:5984")


def load_jsons(resources_path):
    json_files = glob.glob(os.path.join(resources_path, "*.json"))

    jsons = []
    for json_file in json_files:
        with open(json_file) as f:
            jsons.append((json_file, json.load(f)))

    return jsons
