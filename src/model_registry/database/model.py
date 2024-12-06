"""This module contains the definition of the database schema of our application, as well as the definition of the
database connector that is used through the whole package """

from peewee import Model, CharField, ForeignKeyField,PostgresqlDatabase, IntegerField, FloatField
from yaml import safe_load
import pkgutil

# Loading config file
config_file = pkgutil.get_data("model_registry.database","config.yaml")
config = safe_load(config_file)
credentials = config["database_credentials"]

# Defining database connector
# database_uri, user and password are defined in config.yaml
database = PostgresqlDatabase(credentials["db_uri"],user=credentials["username"],password=credentials["password"])


# As per peewe doc -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database

# Note: When no primary key is indicated, peewee automatically creates an incremental id field that will be primary key
class Algorithm(BaseModel):
    name = CharField()


class MlModel(BaseModel):
    name = CharField(unique=True)
    description = CharField()
    status = CharField()
    version = IntegerField()
    image = CharField()
    input_shape = CharField()
    dtype = CharField()
    algorithm = ForeignKeyField(Algorithm)

# Note: The term "parameter" is used in this context to indicate the hyper-params of the model
class Parameter(BaseModel):
    param_name = CharField()
    param_description = CharField()
    dtype = CharField()

class ModelParameter(BaseModel):
    model = ForeignKeyField(MlModel)
    parameter = ForeignKeyField(Parameter)
    parameter_value = FloatField()
    max_threshold = FloatField()
    min_threshold = FloatField()

# This is a reference to all the tables of the schema that is used in the validation.py module
tables = [Algorithm,MlModel,Parameter,ModelParameter]


