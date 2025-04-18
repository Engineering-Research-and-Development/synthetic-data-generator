# Generator Folder Structure

The generator folder contains the source code for the AI-LIB's data generation models and the server API.

## Project Structure

The generator folder is structured as follows:

* `ai_lib/`: Contains the source code for the AI-LIB's data generation models.
	+ `data_generator/`: Contains the source code for the models and the data generation logic.
		- `models/`: Contains the source code for the models.
			- `keras/`: Contains the source code for the Keras-based models.
				- `implementation/`: Contains the source code for the model implementations.
    + `preprocess/`: Contains the source code for the preprocessing logic.
    + `evaluate/`: Contains the source code for synthetic data evaluation logic.
    + `test/`: Contains the source code for the tests.
* `server/`: Contains the source code for the server API.
	+ `app.py`: Contains the source code for the FastAPI application.
  	+ `test/`: Contains the source code for the tests.

