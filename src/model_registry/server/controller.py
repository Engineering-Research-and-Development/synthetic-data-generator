"""This module is the main entry point of FASTApi. It also defines the life-cycle of the application as well as
the database initialization on startup"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from model_registry.database.model import  check_all_database_tables, is_database_empty,populate_db_with_mock_data
from model_registry.server.routers import system_models,trained_models,model_versions,training_info
from yaml import safe_load
import pkgutil

# Loading config file
config_file = pkgutil.get_data("model_registry.server","config.yaml")
config = safe_load(config_file)
server_config = config["server_startup_configuration"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPIcls application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
    # Checking if database exists and has data in int
    if check_all_database_tables() is False or is_database_empty() or server_config["reset_database"]:
        # The ANSI escape sequence are for coloring the text
        if server_config["reset_database"]:
            print("\033[94mDATABASE\033[0m: Dataset is being reset due to server config file flag")
        else:
            print("\033[94mDATABASE\033[0m: Database is empty. Populating it with mock data")
        populate_db_with_mock_data()
    else: print("\033[94mDATABASE\033[0m: Database ready!")
    yield
    #  This part is done after the FASTAPI application is run


# Program entry point
app = FastAPI(lifespan=lifespan)
# Adding routers for model specific request
# i.e A client asks for a specific trained/system model this endpoints will serve that
app.include_router(system_models.router)
app.include_router(trained_models.router)
app.include_router(model_versions.router)
app.include_router(training_info.router)

# The following functions will serve as the mains interface for the client layer
@app.get("/models")
async def controller_get_all_models() -> dict:
    """
    This function represent the main interface for client layer and it returns all the models present in the repository.
    :return: A dictionary containing a list of System Models and Trained Models present in the repository
    """
    sys_models = await system_models.get_all_system_models()
    train_models = await trained_models.get_all_trained_models()
    return {"system_models":sys_models , "trained_models":train_models}




