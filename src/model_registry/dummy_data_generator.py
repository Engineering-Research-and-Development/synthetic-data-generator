"""In the MCS architectural style, the Model represents the core data or business logic of the application.
It is responsible for accessing and manipulating the application's data."""
import random
from datetime import datetime
from random import shuffle
from typing import Type

from sqlmodel import Session, SQLModel

from model_registry.database.schema import SystemModel, TrainedModel, DataType, AllowedDataType, FeatureSchema, \
    TrainingInfo, ModelVersion


def save_data_from_dict(engine, data_class: Type[SQLModel],values: list[dict]):
    """
    This function creates and commits to the database instance of SQLModel class filled with data passed from values
    :param data_class: The class of the data that this function wants to create and commit
    :param values: the data to fill the instances with
    :return:
    """
    # First let's create all the instances of the class
    instances = [data_class(**data) for data in values]
    # Then we add them to the session
    with Session(engine) as session:
        for instance in instances:
            session.add(instance)
        session.commit()

def populate_db_with_mock_data(engine):
    """
    This function populates the database with mock data
    :return: None
    """
    systems,trained_models,data_type,allowed_type,feature_schema,training_info,model_version = create_mock_data()
    save_data_from_dict(engine, SystemModel,systems)
    save_data_from_dict(engine, TrainedModel,trained_models)
    save_data_from_dict(engine, DataType,data_type)
    save_data_from_dict(engine, AllowedDataType,allowed_type)
    save_data_from_dict(engine, FeatureSchema,feature_schema)
    save_data_from_dict(engine, TrainingInfo,training_info)
    save_data_from_dict(engine, ModelVersion,model_version)


default_system_models = [
'Multilayer Perceptron (MLP)',
'Convolutional Neural Networks (CNN)',
'Recurrent Neural Networks (RNN)',
'Generative Adversarial Networks (GAN)',
'Variational Autoencoders (VAEs)',
'T-VAEs',
'Transformers',
'Diffusion Models',
]


def create_system_models_data(batch_size: int = len(default_system_models)) -> list[dict]:
    """
    This function create batch_size mock system_models' data.
    module but this function can handle any batch_size value.
    :param: batch_size.
    :return: A list of system models' information in a form of a dictionary
    """
    if batch_size <= len(default_system_models):
        return  [{"name" : default_system_models[i],"description":"A default description","loss_function":"A loss function"} for i in range(batch_size)]
    else:
        # This is the case when the batch size is bigger than the algorithms names
        # Since the name must be unique we create a name with a random value
        # First we add all the algorithm names indicated in the list
        system_models = [{"name":i,"description":"A default description","loss_function":"A loss function"} for i in default_system_models]
        # We then create N random unique numbers. N is how many numbers we need to get to batch size
        N = batch_size - len(system_models)
        rand_nums = random.sample(range(1, 100), N)
        # Construct a new list by picking a random algo name and concat with random value
        return system_models + [{"name" : (random.choice(system_models)['name'] + str(i)),"description":"A default description","loss_function":"A loss function"} for i in rand_nums]


def create_trained_models_data(batch_size: int = len(default_system_models)) -> list[dict]:
    """
    Creates a list of trained models data of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of trained models data information in a form of a dictionary
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    models = []
    ids = [i for i in range(1,batch_size + 1)]
    shuffle(ids)
    for id in ids:
        random_shape = '(' + str(random.randint(1, 10)) + "x" + str(random.randint(1, 10)) + "x" + str(
            random.randint(1, 10)) + "x" + str(random.randint(1, 10)) + ")"
        models.append({"name":'model' + str(id),"dataset_name":'A dataset',"size":'18B'
                ,"input_shape" : random_shape, "algorithm_name":random.choice(default_system_models)})
    return models


def create_data_type_data() -> list[dict]:
    return[{"type":'string',"is_categorical":True},{"type":'int',"is_categorical":True},{
        "type":'float',"is_categorical":True},{"type":'long_int',"is_categorical":True},{"type":'long_float',"is_categorical":True}]


def create_allowed_data_type_data(batch_size: int = len(default_system_models)) -> list[dict]:
    """
    Creates a list allowed data types of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of allowed data types' information in a form of a dictionary
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    return [{"algorithm_name":random.choice(default_system_models),"datatype":1} for i in range(1,batch_size)]


def create_feature_schema_data(batch_size: int = len(default_system_models)) -> list[dict]:
    """
    Creates a list feature schema data of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of feature schema data types' information in a form of a dictionary
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    ids = [i for i in range(1, batch_size)]
    # For each id create a random data
    data = [{  "feature_name": "A name","feature_position": 0,"is_categorical": False,"trained_model_id": id, "datatype_id": 1} for id in ids]
    # For testing purposes we add some more features for a trained mode
    single_feature_schema = [{  "feature_name": "A name","feature_position": x,"is_categorical": False,"trained_model_id": 1, "datatype_id": 1} for x in range(1,9)]
    return data + single_feature_schema


def create_training_info_data(batch_size: int = len(default_system_models)) -> list[dict]:
    """
    Creates a list of training info  data of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param batch_size: int. Non-negative and greater than 0
    :return: A list of training info  datas' information in a form of a dictionary
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')
    return [{  "loss_function": "A loss function","train_loss_value": random.randint(0,100),
               "val_loss_value":  random.randint(0,100),"n_train_samples":  random.randint(0,100),
               "n_validation_samples":  random.randint(0,100)} for i in range(batch_size)]


def create_model_version_data(batch_size: int = len(default_system_models),nums_multiple_versions: int = 2,
                              num_versions: int = 2):
    """
    Creates a list model version data of dimension batch_size. The value of batch_size must be an integer non-negative and
    greater than 0
    :param: batch_size: int. Non-negative and greater than 0
    :param: nums_multiple_versions: Optional Integer. The number of trained models that have multiple versions.
    :param: num_versions: Optional Integer. The number of multiple versions to create for a random trained model.
    :return: A list of model version data types' information in a form of a dictionary
    :raises: ValueError
    """
    if batch_size <= 0:
        raise ValueError('Batch_size must be greater than 0')

    ids = [i for i in range(1, batch_size + 1)]
    data =  [{ "trained_model_id": id, "training_info_id": id,"version_name":"A name","model_image_path":"fC:\\foo\\bar",
              "timestamp":'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())} for id in ids]
    random_ids = random.choices(ids,k=nums_multiple_versions)
    # Creating for a single model more versions so that testing can be conducted
    multiple_versions = []
    # Train ids start from the last id version
    train_id = batch_size + 1
    for id in random_ids:
        for x in range(nums_multiple_versions * num_versions):
            multiple_versions.append({ "trained_model_id": id, "training_info_id": train_id,"version_name":"A name " + str(x),"model_image_path":"fC:\\foo\\bar",
              "timestamp":'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())})
            train_id += 1
    training_info = create_training_info_data(train_id - 1)
    return data + multiple_versions,training_info


def create_mock_data(batch_size: int = len(default_system_models)):
    versions, training_info = create_model_version_data(batch_size)
    return create_system_models_data(batch_size),create_trained_models_data(batch_size),\
            create_data_type_data(),create_allowed_data_type_data(batch_size),\
            create_feature_schema_data(batch_size),training_info, versions
