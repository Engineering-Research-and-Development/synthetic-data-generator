import numpy as np
from abc import ABC, abstractmethod

from ai_lib.Dataset import Dataset
from ai_lib.Exceptions import ModelException


class UnspecializedModel(ABC):
    def __init__(self, metadata: dict, model_name: str, input_shape: str = None):
        self.metadata = metadata
        self.model_name = model_name
        self.input_shape = input_shape
        self.model = None  # Placeholder for the model instance
        self.scaler = None  # Placeholder for model scaler
        self.training_info = None  # Placeholder for training info
        self.model_misc = None  # Placeholder for model miscellaneous info
        self._parse_shape(self.input_shape)

    @abstractmethod
    def build(self, input_shape: str):
        raise NotImplementedError

    @abstractmethod
    def load(self, model_filepath: str):
        """Load pre-trained weights."""
        raise NotImplementedError

    @abstractmethod
    def _scale(self, data: np.array):
        """Scale inputs with its logic"""
        raise NotImplementedError

    @abstractmethod
    def _inverse_scale(self, data: np.array):
        """Inverse scale inputs with its logic"""
        raise NotImplementedError

    @abstractmethod
    def _pre_process(self, data: Dataset, **kwargs):
        """Pre-process data"""
        raise NotImplementedError

    @abstractmethod
    def train(self, data, **kwargs):
        """Train the model."""
        raise NotImplementedError

    @abstractmethod
    def fine_tune(self, data: np.array, **kwargs):
        """Fine-tune the model."""
        raise NotImplementedError

    @abstractmethod
    def infer(self, n_rows: int, **kwargs):
        """Run inference."""
        raise NotImplementedError

    @abstractmethod
    def save(self, **kwargs):
        """Save Model."""
        raise NotImplementedError

    @classmethod
    def self_describe(cls):
        raise NotImplementedError

    @staticmethod
    def _parse_stringed_input_shape(stringed_shape: str) -> tuple[int, ...]:
        """
        Parses a stringed list of numbers into a tuple

        :param stringed_shape: a stringed list of number in format "[x,y,z]"
        :return: a tuple of numbers, in format (x, y, z)
        """
        brackets = ["(", ")", "[", "]", "{", "}"]
        for b in brackets:
            stringed_shape = stringed_shape.replace(b, "")
        return tuple([int(n) for n in stringed_shape.split(",") if n != ""])

    def _parse_shape(self, input_shape: str):
        try:
            tuple_shape = self._parse_stringed_input_shape(input_shape)
            self.input_shape = tuple_shape
        except ValueError:
            raise ModelException("Cannot build the model, missing input shape")
