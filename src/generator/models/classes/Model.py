import os

from utils.model_utils import parse_stringed_input_shape
from utils.structure import MODEL_FOLDER

from abc import ABC, abstractmethod
from traceback import print_tb

class UnspecializedModel(ABC):
    def __init__(self, metadata:dict, model_name:str, model_filepath:str=None):
        self.metadata = metadata
        self.model_name = model_name
        self.model_filepath = model_filepath
        self.input_shape = None # Placeholder for tuple input shape
        self.parse_metadata()
        self.model = None  # Placeholder for the model instance
        self.scaler = None # Placeholder for model scaler


    def parse_metadata(self):
        metadata = self.metadata
        try:
            self.input_shape = parse_stringed_input_shape(metadata.get("input_shape", ""))
        except ValueError as e:
            print_tb(e.__traceback__)
            print("Data is missing from request", e)


    def initialize(self):
        if self.model_filepath:
            print(f"Loading pre-trained model: {self.model_filepath}")
            model, scaler = self.load()
            self.model = model
            self.scaler = scaler
        else:
            print(f"Building model from scratch: {self.model_name}")
            self.model = self.build(self.input_shape)


    def _check_folder_latest_version(self):
        my_folders_versions = [int(fold.split(":")[1]) for fold in os.listdir(MODEL_FOLDER) if self.model_name in fold]
        if len(my_folders_versions) > 0:
            return max(my_folders_versions)
        else:
            return 0


    @abstractmethod
    def build(self, input_shape):
        """Build the model.
        :param input_shape:
        """
        pass

    @abstractmethod
    def load(self):
        """Load pre-trained weights."""
        pass

    @abstractmethod
    def train(self, data, **kwargs):
        """Train the model."""
        pass

    @abstractmethod
    def fine_tune(self, data, **kwargs):
        """Fine-tune the model."""
        pass

    @abstractmethod
    def infer(self, n_rows:int, **kwargs):
        """Run inference."""
        pass

    @abstractmethod
    def save(self, **kwargs):
        """Run inference."""
        pass
