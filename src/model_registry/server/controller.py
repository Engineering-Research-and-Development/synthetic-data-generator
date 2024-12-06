import peewee
from fastapi import FastAPI,HTTPException,Header,Path
from contextlib import asynccontextmanager
from typing import List, Annotated


from model_registry.database.model import database
from model_registry.database.mock_data_generator import populate_db_with_mockdata
from model_registry.server import service
from model_registry.server.validation import MlModelIn, MlModelOut, TypeAdapter, ValidHeaders, ModifyMlModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPIcls application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
    # Trying to connect to database to check if it simply exists
    database.connect()
    database.close()
    # If database exists, check if tables are present and have data
    if len(database.get_tables()) == 0 or service.is_database_empty():
        # The ANSI escape sequence are for coloring the text
        print("\033[94mDATABASE\033[0m:\tDatabase is empty. Populating it with mock data")
        populate_db_with_mockdata()
    else: print("\033[94mDATABASE\033[0m:\t Database found!")
    yield
    #  This part is done after the FASTAPI application is run


# Program entry point
app = FastAPI(lifespan=lifespan)



@app.post("/models",status_code=201)
async def create_model(input_model: MlModelIn):
    # First step: check if the Algorithm id is valid
    try:
        # TODO: This could be changed so that the whole algorithm can be passed for model creation instead of
        #  retrieving it
        algorithm = service.get_algorithm_by_id(input_model.algorithm)
        service.create_model(input_model, algorithm)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail='An algorithm with id ' + str(input_model.algorithm) + ' does not exist!')
    except peewee.IntegrityError:
        raise HTTPException(status_code=400,detail="A model with the name passed already exists. Model's name must"
                                                   " be unique")



@app.get("/models",status_code=200)
# TODO: I suspect the pydantic validation causes a N + 1 query to validate the data. This is not
#  optimal and should be fixed - Chiedi a Fabio
async def get_models():
        return TypeAdapter(List[MlModelOut]).validate_python(service.get_all_models())


@app.get("/models/{model_id}",status_code=200)
async def get_model(model_id: int,x_client_type: Annotated[ValidHeaders,Header()]):
    """
    This fetches a model by the given id from the model repository. The information returned is dictated
    by the value of x_client_type the defines the used DTO by the function. For more information about the DTOs
    see validation.py
    :param x_client_type: set the DTO needed. Values can be 'frontend','input_coherence','generator'
    :return: A list of models
    """
    try:
            model = service.get_model_by_id(model_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code=404,detail="A model with this id has not been found!")
    # If the model is found choose an appropriate DTO based on the client
    if x_client_type == 'input_coherence':
        validated_model = TypeAdapter(MlModelOut).validate_python(model)
        print(validated_model)
        return {"image":validated_model.image,"algorithm":validated_model.algorithm}
    elif x_client_type == 'generator':
        pass



@app.put("/models/{model_id}",status_code=200)
async def update_model(model_id: int,update_data: ModifyMlModel):
    try:
        return service.update_model(model_id, update_data)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="A model with this id does not exist!")


@app.delete("/models/{model_id}",status_code=200)
async def delete_model(model_id: int):
    try:
        service.delete_model(model_id)
    except peewee.DoesNotExist:
        raise HTTPException(status_code = 404, detail="A model with this id does not exist!")





