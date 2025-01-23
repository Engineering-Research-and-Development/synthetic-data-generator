import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

username = os.environ.get("db_username", "postgres")
password = os.environ.get("db_password", "postgres")
host = os.environ.get("db_host", "localhost")
database = os.environ.get("db_name", "postgres")
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:5432/{database}",echo=False)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
