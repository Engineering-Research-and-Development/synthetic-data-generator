import os

from peewee import *
from datetime import datetime

username = os.environ.get("db_username", "postgres")
password = os.environ.get("db_password", "postgres")
host = os.environ.get("db_host", "localhost")
database = os.environ.get("db_name", "postgres")
init_db = os.environ.get("INIT_DB", False)
db = PostgresqlDatabase(database=database, host=host, user=username, password=password)


class BaseModelPeewee(Model):
    class Meta:
        database = db

class SystemModel(BaseModelPeewee):
    name = CharField(unique=True)
    description = CharField()
    loss_function = CharField()

class DataType(BaseModelPeewee):
    id = AutoField()
    type = CharField()
    is_categorical = BooleanField()

class AllowedDataType(BaseModelPeewee):
    id = AutoField()
    algorithm_name = ForeignKeyField(SystemModel, backref='allowed_data_types')
    datatype = ForeignKeyField(DataType, backref='allowed_data_types')

class TrainedModel(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    dataset_name = CharField()
    size = CharField()
    input_shape = CharField()
    algorithm_name = ForeignKeyField(SystemModel, backref='trained_models')

class Features(BaseModelPeewee):
    id = AutoField()
    feature_name = CharField()
    datatype = ForeignKeyField(DataType, backref='features')
    feature_position = IntegerField()
    trained_model = ForeignKeyField(TrainedModel, backref='features')

class TrainingInfo(BaseModelPeewee):
    id = AutoField()
    loss_function = CharField()
    train_loss_value = DoubleField()
    val_loss_value = DoubleField()
    n_train_sample = IntegerField()
    n_validation_sample = IntegerField()

class ModelVersion(BaseModelPeewee):
    id = AutoField()
    version_name = CharField()
    model_image_path = CharField()
    timestamp = DateTimeField(default=datetime.now)
    trained_model = ForeignKeyField(TrainedModel, backref='model_versions')
    training_info = ForeignKeyField(TrainingInfo, backref='model_versions')
