# Models

## Model Structure

To better understand how to develop new models, it is necessary to understand the folder structure inside `data_generator`:

* `models/`: Contains the source code for the models.
  + `UnspecializedModel.py`: Contains source code for class representing the parent of each model
  + `ModelInfo.py`: Contains source code for class describing models metadata
  + `TrainingInfo.py`: Contains source code for class representing training info
  + `keras/`: Contains the source code for Keras framework models.
    + `<ModelCategory>.py` Contains the source code for a category of models, inheriting from UnspecializedModel and useful to specialize in other submodels
    + `implementation/`: Contains Specific implementations (real blueprints)
      - `<ModelName>.py`: Contains the source code for the model implementation.
* `model_factory.py`: Contains the source code to istantiate models.


## Add a new Blueprint Model to the Generator

Adding a new model requires to follow some simple rules of thumb:
* All implemented models should be subclasses of the `UnspecializedModel` class.

* All implementation models should reside in an "implementation" leave folder for automatic retrieving
  * Intermediate Models describing a Model Category **have to** reside outside implementation folders.
    
* All implementations must implement (override) **ALL** methods from `UnspecializedModel`
  * `_load`: A method to the model objects from a folder. Its role is to populate the `_model` attribute of a class, as well as all optional objects.
  * `_build`: A method to build the model architecture and populates the `_model` attribute.
  * `_instantiate`: A method to instantiate the model: loads the saved model if the load_path is given using `_load`, otherwise build a new one using `_build`
  * `_pre_process`: A method to preprocess the input data for training. It may include shape resizing, scaling, etc.
  * `_scale`: TO BE REMOVED
  * `_inverse_scale`: TO BE REMOVED
  * `set_hyperparameters`: A method to set hyperparameters for specific implemntations
  * `_train`: A method to train the model. After training, the `training_info` attribute should be populated during training using the `TrainingInfo` class.
  * `fine_tune`: OPTIONAL
  * `infer`: A method to call the model to generate synthetic data.
  * `save`: A method to save the model weights and accessories (like scalers) to a file.
  * `self_describe`: A method to provide metadata about the model using the `ModelInfo` class.
 
* A valid implementation should have the following attributes populated:
  * `model_name`: The model name, used to identify the model itself.
  * `input_shape`: A tuple containing the input shape of the model.
  * `training_info`: An instance of the `TrainingInfo` class, containing information about the training process.
  * `_model`: The model object.
  * `_load_path`: The path to load the model from (optional)
