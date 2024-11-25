from utils.model_utils import parse_stringed_input_shape

from abc import ABC, abstractmethod
from traceback import print_tb

class UnspecializedModel(ABC):
    def __init__(self, metadata:dict, model_name:str, weights_path:str=None):
        self.metadata = metadata
        self.model_name = model_name
        self.weights_path = weights_path
        self.input_shape = None # Placeholder for tuple input shape
        self.parse_metadata()
        self.model = None  # Placeholder for the model instance


    def parse_metadata(self):
        metadata = self.metadata
        try:
            self.input_shape = parse_stringed_input_shape(metadata.get("input_shape", ""))
        except ValueError as e:
            print_tb(e.__traceback__)
            print("Data is missing from request", e)


    def initialize(self):
        if self.weights_path:
            print(f"Loading pre-trained model: {self.weights_path}")
            self.model = self.load(self.weights_path)
        else:
            print(f"Building model from scratch: {self.model_name}")
            self.model = self.build(self.input_shape)

    @abstractmethod
    def build(self, input_shape):
        """Build the model.
        :param input_shape:
        """
        pass

    @abstractmethod
    def load(self, weights_path):
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
    def infer(self, n_rows, **kwargs):
        """Run inference."""
        pass