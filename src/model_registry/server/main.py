"""This module is the main entry point of FASTApi. It also defines the life-cycle of the application as well as
the database initialization on startup"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from database.schema import SystemModel, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion, \
    db
from dummy_data_generator import insert_data
from routers import datatypes#, system_models, trained_models, model_versions, training_info, models


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
    db.create_tables([SystemModel, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion])

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

# Adding routers for model specific request
# i.e A client asks for a specific trained/system model this endpoints will serve that
app.include_router(datatypes.router)
#app.include_router(system_models.router)
#app.include_router(trained_models.router)
#app.include_router(model_versions.router)
#app.include_router(training_info.router)
#app.include_router(models.router)

@app.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")