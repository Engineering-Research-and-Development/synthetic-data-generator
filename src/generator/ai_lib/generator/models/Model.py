import os
import shutil

from abc import ABC, abstractmethod

from ai_lib.Exceptions import ModelException


class UnspecializedModel(ABC):
    def __init__(self, metadata: dict, model_name: str, input_shape: str = "", model_filepath: str = None):
        self.metadata = metadata
        self.model_name = model_name
        self.model_filepath = model_filepath
        self.input_shape = None
        self.model = None  # Placeholder for the model instance
        self.scaler = None  # Placeholder for model scaler
        self.training_info = None  # Placeholder for training info
        self.model_misc = None  # Placeholder for model miscellaneous info
        self._parse_shape(input_shape)

    def rollback_latest_version(self, model_folder: str):
        last_folder = os.path.join(model_folder, self.get_last_folder(model_folder))
        print(last_folder)
        if os.path.isdir(last_folder):
            shutil.rmtree(last_folder)
            print("Deleted")

    def check_folder_latest_version(self, model_folder: str):
        root_folder = self._get_model_root_folder()
        my_folders_versions = [int(fold.split(":")[1]) for fold in os.listdir(model_folder) if root_folder in fold]
        if len(my_folders_versions) > 0:
            return max(my_folders_versions)
        else:
            return 0

    def get_last_folder(self, model_folder: str):
        """
        Returns the name of the latest version image of the model
        :return:
        """
        root_folder = self._get_model_root_folder()
        version = self.check_folder_latest_version(model_folder)
        latest_version_folder = f"{root_folder}:{version}"
        return latest_version_folder

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
    def scale(self, data):
        """Scale inputs with its logic"""
        pass

    @abstractmethod
    def inverse_scale(self, data):
        """Inverse scale inputs with its logic"""
        pass

    @abstractmethod
    def pre_process(self, data, **kwargs):
        """Pre-process data"""

    @abstractmethod
    def train(self, data, **kwargs):
        """Train the model."""
        pass

    @abstractmethod
    def fine_tune(self, data, **kwargs):
        """Fine-tune the model."""
        pass

    @abstractmethod
    def infer(self, n_rows: int, **kwargs):
        """Run inference."""
        pass

    @abstractmethod
    def save(self, **kwargs):
        """Save Model."""
        pass

    @classmethod
    def self_describe(cls):
        pass

    def _get_model_root_folder(self):
        """
        Returns the basename of the folder, formed with Class Name + Model Name
        :return:
        """
        class_name = type(self).__name__
        root_folder = f"{class_name}__{self.model_name}"
        return root_folder

    def _create_new_version_folder(self, model_folder:str):
        new_version = self.check_folder_latest_version(model_folder) + 1
        root_folder = self._get_model_root_folder()
        new_version_folder = f"{root_folder}:{new_version}"
        save_folder = os.path.join(model_folder, new_version_folder)

        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)

        return save_folder

    @staticmethod
    def parse_stringed_input_shape(stringed_shape: str) -> tuple[int, ...]:
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
            tuple_shape = self.parse_stringed_input_shape(input_shape)
            self.input_shape = tuple_shape
        except ValueError:
            raise ModelException("Cannot build the model, missing input shape")

    def _initialize(self):
        if self.model_filepath:
            print(f"Loading pre-trained model: {self.model_filepath}")
            try:
                model, scaler = self.load()
            except Exception:
                raise ModelException("Model file not found")
            self.model = model
            self.scaler = scaler
        else:
            print(f"Building model from scratch: {self.model_name}")
            self.model = self.build(self.input_shape)
