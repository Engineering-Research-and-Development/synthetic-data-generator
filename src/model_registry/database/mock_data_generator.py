""" This module offers mock-data generating methods. This module should be called once before launching the FASTApi
server in order to populate the db and to not waste any time in application startup"""

from random import shuffle
import random
from model_registry.database.model import Algorithm, MlModel, Parameter, ModelParameter, database
from model_registry.server import service

algorithm_names = [
'Linear Regression',
'Random Forest Regression',
'XGBoost',
'LightGBM',
'CatBoost',
'Bayesian Regression',
'K-NN Regression',
'Logistic Regression',
'Support Vector Machines (SVM)',
'K-Nearest Neighbors (KNN) Classification',
'Decision Trees',
'Random Forest Classification',
'Gradient Boosting Machines (GBM)'
]


def create_mock_algorithms(batch_size: int = len(algorithm_names)) -> list[Algorithm]:
    """
    This function create batch_size mock algorithms' data. Batch_size default value is defined in mock_data_generator.py
    module but this function can handle any batch_size value
    :param batch_size: int.
    :return: A list of Algorithms
    """
    if batch_size <= len(algorithm_names):
        return  [Algorithm(name=algorithm_names[i]) for i in range(batch_size)]
    else:
        # This is the case when the batch size is bigger than the algorithms names
        # Since the name must be unique we create a name with a random value
        # First we add all the algorithm names indicated in the list
        algorithms = [Algorithm(name=i) for i in algorithm_names]
        # We then create N random unique numbers. N is how many numbers we need to get to batch size
        N = batch_size - len(algorithms)
        rand_nums = random.sample(range(1, 100), N)
        # Construct a new list by picking a random algo name and concat with random value
        return algorithms + [Algorithm(name=(random.choice(algorithm_names) + str(i))) for i in rand_nums]



def create_mock_models(batch_size: int = len(algorithm_names)) -> list[MlModel]:
    """
    Creates a list of models of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of MlModels
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    models = []
    ids = [i for i in range(1,batch_size)]
    shuffle(ids)
    for id in ids:
        random_shape = '(' + str(random.randint(1, 10)) + "x" + str(random.randint(1, 10)) + "x" + str(
            random.randint(1, 10)) + "x" + str(random.randint(1, 10)) + ")"
        models.append(MlModel(name='model' + str(id),description='A description',status='Blank',version=1,image='rC:\\foo\\bar'
                ,input_shape = random_shape, dtype='string',algorithm=id))
    return models


def create_mock_params(batch_size: int = len(algorithm_names)) -> list[Parameter]:
    """
    Creates a list of parameters of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of MlModels
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    return[Parameter(param_name='param' + str(i),param_description='A description',dtype='A type') for i in range(1,batch_size)]


def create_mock_model_params(batch_size: int = len(algorithm_names)) -> list[ModelParameter]:
    """
    Creates a list of model parameters of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of MlModels
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    ids = [i for i in range(1,batch_size)]
    return [ModelParameter(model=id,parameter=id,parameter_value=20,max_threshold=20,min_threshold=20) for id in ids]


def create_mock_data(batch_size: int = len(algorithm_names)):
    return create_mock_algorithms(batch_size),create_mock_models(batch_size),create_mock_params(batch_size),\
            create_mock_model_params(batch_size)

# This code should be executed only once to populate the database with mock data
if __name__ == '__main__':
    # Open the database connection
    database.connect()
    service.reset_database()
    # Create all the mock data
    algorithms,models,params,model_params = create_mock_data()
    # Push into database
    with database.atomic():
        Algorithm.bulk_create(algorithms)
        MlModel.bulk_create(models)
        Parameter.bulk_create(params)
        ModelParameter.bulk_create(model_params)
    database.close()

