## Model Repository
This module implements a catalogue
who's job is to offer CRUD operations to other modules
that are interested in obtaining info
/ saving ML models.   The repository's structure follows the Model - Controller - Service
architectural style.  
The package is composed of:
### 1. Database folder
![db_schema](db_schema.png)
*The db schema defined by us*   

The database folder contains the database's schema that we have defined for our application.
The main tables of interest are the *System Model* and the *Trained Model* and the meaning
of their relationship. Conceptually, a System Model can be seen as any AI model that 
the Model Repository (from this point forward shorted to MR) wants to keep track. 
In fact, of each model the MR tracks the name, a brief description and the loss function that
the model uses. Each System Model in order to function uses a specific data type and
this behaviour is modeled by the relationship *Allows* with the table *Data Type*.  
A Trained Model refers to a specific AI model's architecture
that a user selects from the System Model and intends to use for some tasks. 
In this context, a Trained Model can be considered an  instance of a System Model. 
While a System Model can have multiple instances of Trained Models, each Trained 
Model can "inherit" the definition of only one System Model. 
For example, a System Model could be a Convolutional Neural Network (CNN), 
and while multiple CNN models with different parameters may exist, they all share the 
same architectural concept.  
A Trained Model in order to exist must have a version that is the result of a training 
process. For this reason, each version must also have a training info.  
It is important to note the relationship between a Trained Model and the table Data Type.
This relationship exists because the same Trained Model can produce different results from the same dataset if 
the order of the input features changes. So this relationship keeps track of how the 
features are passed given a trained model.  

Inside this folder there are also the following files:
*   `data_generator.py` is responsible for the generation and
insertion of fake data inside the database
* `schema.py` is the definition of our db schema with an ORM (in this
case is sqlmodel). The ORM let's us easily create queries that are used by
the service layer
* `model.py` defines how the queries are created and handles the database
connection as well as the retrieval and manipulation of raw data
* `config.yaml` houses the database credentials as well as the name of 
host and of the database to connect to
### 2. Server folder
The server folder houses the implementation of the business logic as
well as the definition of the endpoints that the model registry offers.
This package is organized as the following:
* `routers` is the module responsible for the definition
of the model repository endpoints
* `service` is the module responsible for the implementation of the 
business logic of the application
* `config.yaml` contains variable that determines the behaviour of the 
server on startup
* `validation.py` defines the Pydantic models that the endpoint take in input and
return in output so that they can be automatically validated
### 3. Testing folder
Contains automatic testing code with which the application has been 
tested. In order to replicate the testing that has been done, launch
the `main.py` while the model repository server is running. The main 
will then call all the testing functions present in `test_tmodel.py`
## Configuration files
The following configuration can be found inside the project:
1. `model_registry/server/config.yaml`: Contains
flags that determine the server behaviour on startup
2. `model_registry/database/config.yaml`: Contains information needed for the database connection, like hostname,
database name, and user credentials 
## Docker: How to run it
Download or pull the code, navigate to the code's folder and simply run  
> docker compose up  

This will build the model repository and latest postgres image and
launch a compose stack with both the model repository and postgres
containers. After the containers are launched, you can start sending
request to the endpoints by navigating to http://127.0.0.1:80 and
adding the endpoints name!
## OpenAPI Documentation
As default, FASTApi will automatically create the documentation when 
the server is launched at http://127.0.0.1/docs.  