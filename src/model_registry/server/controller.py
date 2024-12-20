from xmlrpc.client import Error

from fastapi import FastAPI,Header
from typing import Annotated
from contextlib import asynccontextmanager
from model_registry.database.model import  check_all_database_tables, is_database_empty,populate_db_with_mock_data
from model_registry.server.routers import system_models,trained_models,model_versions
from model_registry.server.validation import ValidHeaders

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPIcls application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
    # Checking if database exists and has data in int
    if check_all_database_tables() is False or is_database_empty() :
        # The ANSI escape sequence are for coloring the text
        print("\033[94mDATABASE\033[0m:\tDatabase is empty. Populating it with mock data")
        populate_db_with_mock_data()
    else: print("\033[94mDATABASE\033[0m:\t Database found!")
    yield
    #  This part is done after the FASTAPI application is run


# Program entry point
app = FastAPI(lifespan=lifespan)
# Adding routers for model specific request
# i.e A client asks for a specific trained/system model this endpoints will serve that
app.include_router(system_models.router)
app.include_router(trained_models.router)
app.include_router(model_versions.router)

# The following functions will serve as the mains interfaces that clients will go to
@app.get("/models")
async def controller_get_all_models():
     sys_models = await system_models.get_all_system_models()
     train_models = await trained_models.get_all_system_models()
     return {"system_models":sys_models , "trained_models":train_models}


@app.get("/models/{model_id}")
async def controller_get_model(model_id: int,x_content_type: Annotated[str,Header()]):
    pass



