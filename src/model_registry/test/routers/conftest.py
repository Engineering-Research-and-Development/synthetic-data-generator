# import pytest
# import yaml
# from peewee import PostgresqlDatabase
# from database.schema import Algorithm, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion, \
#     db, Parameter, Function, FunctionParameter
# import os
#
# with open('src/model_registry/test/routers/config.yml', 'r') as file:
#     config = yaml.safe_load(file)
#     server = config["server"]
#
#
# @pytest.fixture(scope="module",autouse=True)
# def get_connection():
#     username = os.environ.get("db_username", "postgres")
#     password = os.environ.get("db_password", "postgres")
#     host = os.environ.get("db_host", "localhost")
#     database = os.environ.get("db_name", "postgres")
#     db = PostgresqlDatabase(database=database, host=host, user=username, password=password)
#     db.create_tables([Algorithm, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion,
#                       Function, Parameter, FunctionParameter])
