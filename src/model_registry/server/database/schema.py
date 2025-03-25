import os
from datetime import datetime

from peewee import (
    PostgresqlDatabase,
    Model,
    AutoField,
    CharField,
    BooleanField,
    ForeignKeyField,
    DateTimeField,
    IntegerField,
    DoubleField,
    SQL,
    CompositeKey,
)

username = os.environ.get("db_username", "postgres")
password = os.environ.get("db_password", "postgres")
host = os.environ.get("db_host", "127.0.0.1")
database = os.environ.get("db_name", "postgres")
port = os.environ.get("port", 5432)
db = PostgresqlDatabase(
    database=database, host=host, user=username, password=password, port=port
)


class BaseModelPeewee(Model):
    class Meta:
        database = db


class Algorithm(BaseModelPeewee):
    id = AutoField()
    name = CharField(unique=True)
    description = CharField()
    default_loss_function = CharField()


class DataType(BaseModelPeewee):
    id = AutoField()
    type = CharField()
    is_categorical = BooleanField()

    class Meta:
        constraints  = [SQL('UNIQUE("type", "is_categorical")')]


class AlgorithmDataType(BaseModelPeewee):
    id = AutoField()
    algorithm_id = ForeignKeyField(
        Algorithm, backref="allowed_data_types", on_delete="CASCADE"
    )
    datatype = ForeignKeyField(DataType, backref="allowed_data_types")


class TrainedModel(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    dataset_name = CharField()
    size = CharField()
    input_shape = CharField()
    algorithm_id = ForeignKeyField(
        Algorithm, backref="trained_models", on_delete="CASCADE"
    )


class Features(BaseModelPeewee):
    id = AutoField()
    feature_name = CharField()
    datatype = ForeignKeyField(DataType, backref="features")
    feature_position = IntegerField()
    trained_model = ForeignKeyField(
        TrainedModel, backref="features", on_delete="CASCADE"
    )


class ModelVersion(BaseModelPeewee):
    id = AutoField()
    version_name = CharField()
    image_path = CharField()
    timestamp = DateTimeField(default=datetime.now)
    trained_model = ForeignKeyField(
        TrainedModel, backref="model_versions", on_delete="CASCADE"
    )


class TrainingInfo(BaseModelPeewee):
    id = AutoField()
    loss_function = CharField()
    train_loss = DoubleField()
    val_loss = DoubleField()
    train_samples = IntegerField()
    val_samples = IntegerField()
    model_version_id = ForeignKeyField(
        ModelVersion, backref="training_info", on_delete="CASCADE", unique=True
    )


######
class Function(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    description = CharField()
    function_reference = CharField()


class Parameter(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    value = CharField()
    parameter_type = CharField(constraints=[SQL("CHECK (parameter_type IN ('float'))")])


class FunctionParameter(BaseModelPeewee):
    function = ForeignKeyField(Function, backref="function_parameters")
    parameter = ForeignKeyField(Parameter, backref="function_parameters")

    class Meta:
        primary_key = CompositeKey("function", "parameter")
