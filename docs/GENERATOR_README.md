# Generator Folder Structure

The generator folder contains the source code for the AI-LIB's data generation models and the server API.

## Overall Structure

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

### Model Structure

The models inside data_generator are structured as follows:

* `models/`: Contains the source code for the models.
  + `UnspecializedModel.py`: Contains source code for class representing the parent of each model
  + `ModelInfo.py`: Contains source code for class describing models metadata
  + `TrainingInfo.py`: Contains source code for class representing training info
  + `keras/`: Contains the source code for Keras framework models.
    + `<ModelCategory>.py` Contains the source code for a category of models, inheriting from UnspecializedModel and useful to specialize in other submodels
    + `implementation/`: Contains Specific implementations (real blueprints)
      - `<ModelName>.py`: Contains the source code for the model implementation.
* `model_factory.py`: Contains the source code for the model factory for each model


All implemented models should be subclasses of the `UnspecializedModel` class.
All implementation models should reside in an "implementation" folder for automatic retrieving
All model metadata structure stored in a `ModelInfo` class.

The model implementation should contain the following methods:
* `_train`: Trains the model.
* `infer`: Generates synthetic data using the model.
* `save`: Saves the model weights and accessories (like scalers) to a file.
* `_load`: Loads the model objects from a folder.
* `self_describe`: Returns metadata about the model using the `ModelInfo` class.
* `_build`: Builds the model architecture (implementation specific).
* `_instantiate`: Instantiates the model and loads the saved model if the load_path is given, otherwise build new
* `_pre_process`: Pre-processes the input data for training.

Each new model implementation should also contain the following attributes:
* `model_name`: The model name, used to identify the model itself.
* `input_shape`: A tuple containing the input shape of the model.
* `training_info`: An instance of the `TrainingInfo` class, containing information about the training process.
* `model`: The model object.
* `scaler`: The scaler object. (optional)
* `load_path`: The path to load the model from (optional)

Each model implementation should be tested using `pytest` 


### Server Structure

The server API is structured as follows:

* `app.py`: Contains the source code for the FastAPI application.
	+ `generator`: The FastAPI application.
		- `train`: The train endpoint.
		- `infer`: The infer endpoint.
	+ `validation_schema`: The validation schema.
		- `TrainRequest`: The train request schema.
		- `InferRequest`: The infer request schema.

