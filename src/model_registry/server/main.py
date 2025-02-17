"""This module is the main entry point of FASTApi. It also defines the life-cycle of the application as well as
the database initialization on startup"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from .database.schema import Algorithm, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion, \
    db, Parameter, Function, FunctionParameter
from .dummy_data_generator import insert_data
from .routers import datatypes, functions,trained_models, algorithm, models
from .routers.sdg_input import user_data

allowed_origins = os.environ.get('allowed_origins', '*').split(',')
allow_credentials = os.environ.get("allow_credentials", True)
allow_methods = os.environ.get("allow_methods", '*').split(',')
allow_headers = os.environ.get("allow_headers", '*').split(',')
init_db = os.environ.get("INIT_DB", False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPIcls application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
    db.create_tables([Algorithm, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion,
                      Function, Parameter, FunctionParameter])

    if init_db:
        insert_data()

    yield
    #  This part is done after the FASTAPI application is run


# Program entry point
app = FastAPI(lifespan=lifespan)
# Authorizing all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

app.include_router(datatypes.router)
app.include_router(user_data.router)
app.include_router(functions.router)
app.include_router(algorithm.router)
app.include_router(trained_models.router)
app.include_router(models.router)

@app.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")
