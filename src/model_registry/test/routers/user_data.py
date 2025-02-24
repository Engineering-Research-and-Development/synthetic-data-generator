import json
from http.client import responses

import requests
from ..conftest import server,port
from copy import deepcopy

endpoint = "/sdg_input"
base_url = f"{server}:{port}{endpoint}"
base_payload = {
   "additional_rows":"1",
   "functions":[
      {
         "feature":"a feature",
         "function_id":"1",
         "parameters":[
            {
               "param_id":"2",
               "value":"1.0"
            }

         ]
      },
      {
         "feature": "a feature",
         "function_id": "2",
         "parameters": [
            {
               "param_id": "3",
               "value": "1.0"
            }
         ]
      },
   ],
   "ai_model":{
      "selected_model_id":"1",
      "new_model":"true",
      "new_model_name":"A name",
      "model_version":"v1.0"
   },
   "user_file":None,
   "features_created":[
      {
         "feature":"A feature",
         "type":"float",
         "category":"continuous"
      },
      {
         "feature": "A feature",
         "type": "float",
         "category": "continuous"
      },
      {
         "feature": "A feature",
         "type": "float",
         "category": "continuous"
      }
   ]

}
### Validation tests
def test_bad_input_additional_row_negative_int():
    payload = deepcopy(base_payload)
    payload['additional_rows'] = "-10"
    response =  requests.post(base_url,json=payload)
    assert response.status_code == 422, print(response.content)

def test_bad_input_additional_row_positive_float():
   payload = deepcopy(base_payload)
   payload['additional_rows'] = "10.40"
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.content)

def test_bad_input_additional_row_negative_float():
   payload = deepcopy(base_payload)
   payload['additional_rows'] = "-10.40"
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.content)

def test_bad_input_additional_row_bad_type():
   payload = deepcopy(base_payload)
   payload['additional_rows'] = "not a number"
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.content)

def test_bad_input_additional_row_zero_input():
   payload = deepcopy(base_payload)
   payload['additional_rows'] = "0"
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.content)

def test_bad_input_additional_row_math_expr():
   payload = deepcopy(base_payload)
   payload['additional_rows'] = "0 + 5"
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.content)

def test_bad_input_function_list_empy():
   payload = deepcopy(base_payload)
   payload['functions'] = []
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.text)

def test_bad_input_function_empty_feature():
   payload = deepcopy(base_payload)
   payload['functions'][0]['feature'] = ' '
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_function_starting_empty_string():
   payload = deepcopy(base_payload)
   payload['functions'][0]['feature'] = ' a string'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_function_leading_empty_string():
   payload = deepcopy(base_payload)
   payload['functions'][0]['feature'] = 'a string '
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_function_bad_function_id_type():
   payload = deepcopy(base_payload)
   payload['functions'][0]['function_id'] = 'a string instead of int'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_function_bad_function_id_negative():
   payload = deepcopy(base_payload)
   payload['functions'][0]['function_id'] = '-10'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_function_bad_function_id_zero():
   payload = deepcopy(base_payload)
   payload['functions'][0]['function_id'] = '0'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_params_empty_list():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'] = []
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.text)

def test_bad_input_params_zero_id():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'][0]['param_id'] = '0'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_params_negative_id():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'][0]['param_id'] = '-10'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_params_float_id():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'][0]['param_id'] = '10.10'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_params_negative_float_id():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'][0]['param_id'] = '-10.10'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_params_bad_type_id():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'][0]['param_id'] = 'not a int'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_input_params_bad_type_value():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'][0]['value'] = 'not a float'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_empty():
   payload = deepcopy(base_payload)
   payload['ai_model'] = None
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_empty_id():
   payload = deepcopy(base_payload)
   payload['ai_model']['selected_model_id'] = ''
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_negative_id():
   payload = deepcopy(base_payload)
   payload['ai_model']['selected_model_id'] = '-10'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_float_id():
   payload = deepcopy(base_payload)
   payload['ai_model']['selected_model_id'] = '-10.20'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_new_model_bad_type_string():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model'] = 'not a boolean'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_new_model_bad_type_int():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model'] = '100'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)


def test_bad_ai_model_new_model_name_bad_string():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model_name'] = ' a name'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_new_model_name_bad_string_leading_space():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model_name'] = 'a name '
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_model_version_bad_string():
   payload = deepcopy(base_payload)
   payload['ai_model']['model_version'] = ' a name'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_bad_ai_model_model_version_bad_string_leading_space():
   payload = deepcopy(base_payload)
   payload['ai_model']['model_version'] = 'a name '
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

def test_exclusivity_userfile_features_create():
   payload = deepcopy(base_payload)
   payload['user_file'] = [{'some_stuff':'some_data'}]
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.text)

### From here we start to create tests that cover the endpoint
def test_bad_functions_less_params():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'] = []
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.text)

def test_bad_functions_same_params():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'].append({"param_id":"2","value":"1.0"})
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400,print(response.content)

def test_bad_functions_bad_params():
   payload = deepcopy(base_payload)
   payload['functions'][0]['parameters'].append({"param_id":"400","value":"1.0"})
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400,print(response.content)

def test_check_ai_model_check_new_model():
   payload = deepcopy(base_payload)
   payload['ai_model']['selected_model_id'] = '1000'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.content)

def test_check_ai_model_check_existing_model_bad_id():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model'] = 'false'
   payload['ai_model']['selected_model_id'] = '1000'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.content)

def test_check_ai_model_check_existing_model_bad_version_name():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model'] = 'false'
   payload['ai_model']['model_version'] = 'A name not present in the db'
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.content)

# Now we test the case where everything should go
def test_check_ai_model_new_model_all_good():
   response = requests.post(base_url,json=base_payload)
   assert response.status_code == 200, print(response.content)

def test_check_ai_model_existing_model_all_good():
   payload = deepcopy(base_payload)
   payload['ai_model']['new_model'] = 'false'
   response = requests.post(base_url,json=payload)
   assert response.status_code == 200, print(response.content)

def test_check_user_file_empty():
   payload = deepcopy(base_payload)
   payload['features_created'] = None
   payload['user_file'] = []
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.content)

def test_check_user_file_categorical():
   payload = deepcopy(base_payload)
   payload['features_created'] = None
   payload['user_file'] = [
      {
         'col1':'X',
         'col2':'X',
         'col3': 'X'
       },
      {
         'col1': 'Y',
         'col2': 'Y',
         'col3': 'Y'
      }
   ]
   response = requests.post(base_url, json=payload)
   assert response.status_code == 400, print(response.content)

def test_check_user_file_continuous_good():
   payload = deepcopy(base_payload)
   payload['features_created'] = None
   payload['user_file'] = [
      {
         'col1':'10',
         'col2':'100',
         'col3': '5'
       },
      {
         'col1': '1',
         'col2': '1',
         'col3': '1'
      }
   ]
   response = requests.post(base_url, json=payload)
   assert response.status_code == 200, print(response.content)

def test_check_features_created_bad_types():
   payload = deepcopy(base_payload)
   payload['features_created'].append(
      {
         "feature": "A feature",
         "type": "Not a supported type",
         "category": "continuous"
      }
   )
   response = requests.post(base_url, json=payload)
   assert response.status_code == 422, print(response.content)

