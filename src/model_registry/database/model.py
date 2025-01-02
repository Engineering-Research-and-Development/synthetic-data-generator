"""In the MCS architectural style, the Model represents the core data or business logic of the application.
It is responsible for accessing and manipulating the application's data."""

from sqlmodel import create_engine,Session,select

from model_registry.database.data_generator import create_mock_data
# This is needed since to create the table we need the models defined in the schema
from model_registry.database.schema import *
from yaml import safe_load
import pkgutil
from sqlalchemy import text, Sequence
from typing import Type

# Loading config file
config_file = pkgutil.get_data("model_registry.database","config.yaml")
config = safe_load(config_file)
credentials = config["database_credentials"]

# Defining database engine and Dialect for connection
engine = create_engine("postgresql+psycopg2://{username}:{password}@localhost:5432/{database}"
                       .format(username=credentials["username"],password=credentials["password"],database=credentials["db_uri"]),echo=False)

def create_database_tables():
    SQLModel.metadata.create_all(engine)

def reset_database():
    """
    This function resets the current database by dropping and recreating the database schema
    :return:
    """
    with engine.connect() as conn:
        result = conn.execute(text("DROP SCHEMA public CASCADE;CREATE SCHEMA public;"))
        conn.commit()
    # After the database has been cleared, recreate all the tables
    create_database_tables()

def check_all_database_tables() -> bool:
    """
    This function checks if all the tables of the database are present
    :return: bool. True if all the tables are present. Otherwise, it returns False
    """

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM information_schema.tables WHERE table_schema = 'public'"))
        print("\033[93mDATABASE INFO\033[0m: Founded ",result.rowcount," tables")
        return True if result.rowcount == len(tables) else False

def is_database_empty() -> bool:
    """
     This function checks that for each table of the database there is data present
    :return: bool. True if the database is empty. Otherwise, it returns False
    """
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f'SELECT * FROM "{table.__name__.lower()}"'))
            print("\033[93mDATABASE INFO\033[0m: For table ",table.__name__.lower(), "founded ",result.rowcount," records")
            if result.rowcount == 0:
                return True
        return False

def save_data(data: SQLModel,refresh_data: bool = False):
    with Session(engine) as session:
        session.add(data)
        session.commit()
        if refresh_data:
            session.refresh(data)

def save_all(data_list: list[SQLModel]):
        with Session(engine) as session:
            for data in data_list:
                session.add(data)
                session.commit()

def select_all(data_class: Type[SQLModel]) -> Sequence[SQLModel]:
    with Session(engine) as session:
        statement = select(data_class)
        results = session.exec(statement)
        return results.all()

def select_data_by_id(data_class: Type[SQLModel],data_id: int):
    with Session(engine) as session:
        statement = select(data_class).where(data_class.id == data_id)
        results = session.exec(statement).one()
        return results

def delete_data_by_id(data_class: Type[SQLModel],data_id: int):
    with Session(engine) as session:
        elem = select_data_by_id(data_class,data_id)
        session.delete(elem)
        session.commit()

def delete_instance(instance: SQLModel):
    with Session(engine) as session:
        session.delete(instance)
        session.commit()

def save_data_from_dict(data_class: Type[SQLModel],values: list[dict]):
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

def populate_db_with_mock_data():
    """
    This function populates the database with mock data from the data_generator.py
    :return: None
    """
    reset_database()
    systems,trained_models,data_type,allowed_type,feature_schema,training_info,model_version = create_mock_data()
    save_data_from_dict(SystemModel,systems)
    save_data_from_dict(TrainedModel,trained_models)
    save_data_from_dict(DataType,data_type)
    save_data_from_dict(AllowedDataType,allowed_type)
    save_data_from_dict(FeatureSchema,feature_schema)
    save_data_from_dict(TrainingInfo,training_info)
    save_data_from_dict(ModelVersion,model_version)

