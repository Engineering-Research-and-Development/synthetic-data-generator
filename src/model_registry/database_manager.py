from playhouse.postgres_ext import *

from model_registry.database_schema import get_schema,MLModel,Algorithm,Metadata
from model_registry.mock_data_generator import create_mock_algorithms, create_mock_models, \
    create_mock_model_metadata


class DatabaseManager:
    def __init__(self,db_type: str = 'postgres',db_uri = 'modelregistry'):
        if db_type != 'postgres':
            raise NotImplemented("Only df_type = postgres is supported")

        self.postgres_db = PostgresqlExtDatabase(db_uri,user='postgres', password='admin')
        if not self.postgres_db.connect():
           raise ConnectionError("Could not connect to database")

        # Bind all classes
        # TODO: This should be done automatically so that the db schema can grow dynamically
        self.tables = get_schema()
        self.postgres_db.bind(self.tables)
        self.postgres_db.create_tables(self.tables)




    def create_mock_data(self,batch_size = 50):
        mock_algorithms = create_mock_algorithms(batch_size)
        mock_models = create_mock_models(batch_size)
        mock_metadata = create_mock_model_metadata(batch_size)
        with self.postgres_db.atomic():
            Algorithm.bulk_create(mock_algorithms)
            Metadata.bulk_create(mock_metadata)
            MLModel.bulk_create(mock_models)




    def delete_all(self):
        self.postgres_db.drop_tables(self.tables)


    def close_connection(self) -> None:
        self.postgres_db.close()


