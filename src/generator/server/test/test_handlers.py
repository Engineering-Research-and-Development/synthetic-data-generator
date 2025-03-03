import requests
from ..middleware_handlers import server_sync_trained, server_sync_algorithms, remote_sync

test_remote_train_db = {
"1": {
"name": "TrainedModel_0",
"dataset_name": "Dataset_0",
"size": "15MB",
"input_shape": "(1,2,3)",
"algorithm_id": 2,
"id": 1,
"algorithm_name": "System_1"
},
"2": {
"name": "TrainedModel_1",
"dataset_name": "Dataset_1",
"size": "30MB",
"input_shape": "(2,3,4)",
"algorithm_id": 3,
"id": 2,
"algorithm_name": "System_2"
},
"3": {
"name": "TrainedModel_2",
"dataset_name": "Dataset_2",
"size": "45MB",
"input_shape": "(3,4,5)",
"algorithm_id": 4,
"id": 3,
"algorithm_name": "System_3"
},
"4": {
"name": "TrainedModel_3",
"dataset_name": "Dataset_3",
"size": "60MB",
"input_shape": "(4,5,6)",
"algorithm_id": 5,
"id": 4,
"algorithm_name": "System_4"
},
"5": {
"name": "TrainedModel_4",
"dataset_name": "Dataset_4",
"size": "75MB",
"input_shape": "(5,6,7)",
"algorithm_id": 1,
"id": 5,
"algorithm_name": "System_0"
},
"6": {
"name": "TestingModel",
"dataset_name": "A dataset",
"size": "100b",
"input_shape": "(19,29,19)",
"algorithm_id": 2,
"id": 6,
"algorithm_name": "System_1"
},
"10": {
"name": "TestingModel",
"dataset_name": "A dataset",
"size": "100b",
"input_shape": "(19,29,19)",
"algorithm_id": 2,
"id": 10,
"algorithm_name": "System_1"
}
}
test_remote__algo_db = {
  "System_0": {
    "name": "System_0",
    "description": "Unique Description 0",
    "default_loss_function": "LossFunction_0",
    "id": 1
  },
  "System_1": {
    "name": "System_1",
    "description": "Unique Description 1",
    "default_loss_function": "LossFunction_1",
    "id": 2
  },
  "System_2": {
    "name": "System_2",
    "description": "Unique Description 2",
    "default_loss_function": "LossFunction_2",
    "id": 3
  },
  "System_3": {
    "name": "System_3",
    "description": "Unique Description 3",
    "default_loss_function": "LossFunction_3",
    "id": 4
  },
  "System_4": {
    "name": "System_4",
    "description": "Unique Description 4",
    "default_loss_function": "LossFunction_4",
    "id": 5
  },
  "TestTest28983": {
    "name": "TestTest28983",
    "description": "A default description",
    "default_loss_function": "A loss function",
    "id": 6
  }
}

local_trains = [  {
    "name": "TrainedModel_" + str(i),
    "dataset_name": "Dataset_" + str(i),
    "size": "75MB",
    "input_shape": "(5,6,7)",
    "algorithm_id": str(i),
    "id": str(i),
    "algorithm_name": "System_0"
  } for i in range(1,10)]
local_algos = [{'name':'System_' + str(i), 'description': 'A description'
                       , 'default_loss_function':'A loss function','folder_path':'server/saved_models/algorithms/i'} for i in range(10)]

def test_server_sync_trained(local_repo_trees):
    tree_trained,_ = local_repo_trees
    server_sync_trained(tree_trained,local_trains)
    local_keys = [int(x['id']) for x in local_trains]
    for key,value in tree_trained.items():
      assert key in local_keys

def test_server_sync_algo(local_repo_trees):
    _,tree_algo = local_repo_trees
    server_sync_algorithms(tree_algo,local_algos)
    local_keys = [x['name'] for x in local_algos]
    for key,value in tree_algo.items():
      assert key in local_keys


def test_intersec_and_integrate_remote_data(local_repo_trees):
    trained_trees, _ = local_repo_trees






