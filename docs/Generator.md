# Generator 

The generator is a tool for generating synthetic data.

The generator is based on the [FastAPI](https://fastapi.tiangolo.com/) framework
and uses [Keras](https://keras.io/) as its deep learning engine. It is designed
to be highly extensible and customizable.

The generator is designed to support a variety of algorithms, ranging from AI models to simple statistical models
The generator also supports a variety of data types, currently includes tabular data and time series data.



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

