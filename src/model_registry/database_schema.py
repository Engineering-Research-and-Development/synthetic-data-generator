from peewee import Model, CharField, ForeignKeyField, SmallIntegerField, \
    CompositeKey
from playhouse.postgres_ext import BinaryJSONField


# Model Repository DB Schema
# Note: When no primary key is indicated, peewee automatically creates an incremental id field that will be primary key
class Algorithm(Model):
    name = CharField()


class Metadata(Model):
    dtype = CharField()
    input_shape = CharField()
    params = BinaryJSONField()
    metrics = BinaryJSONField()

class MLModel(Model):
    name = CharField(unique=True)
    file_path = CharField()
    metadata = ForeignKeyField(Metadata,backref='metadata')


import inspect,sys
def get_schema() -> list:
    # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    clsmembers = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
    classes =  [x[1] for x in clsmembers]
    print("Loaded ",len(classes)," classes from schema")
    return classes