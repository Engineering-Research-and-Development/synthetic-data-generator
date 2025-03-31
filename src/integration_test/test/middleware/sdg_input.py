import json

endpoint = "/sdg_input"

features_payload = json.load(open("../../resources/sdg_input_with_features.json", "r"))
file_payload = json.load(open("../../resources/sdg_input_with_file.json", "r"))