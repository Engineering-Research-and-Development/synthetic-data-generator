import numpy as np
import pandas as pd

from exceptions.DataException import DataException


NUMERICAL = "continuous"
CATEGORICAL = "categorical"
OTHER = "none"


class Dataset:
    def __init__(self, dataset:list[dict]):
        self.dataset: list[dict] = dataset
        self.dataframe: pd.DataFrame = pd.DataFrame()
        self.columns: list[str] = []
        self.continuous_columns = []
        self.categorical_columns = []
        self.unrecognized_columns = []
        self.continuous_data: pd.DataFrame = pd.DataFrame()
        self.categorical_data: pd.DataFrame = pd.DataFrame()
        self.input_shape: str = ""
        self._configure()


    def _configure(self):
        """
            Convert data from requests into an easy-to-process dataframe
            dataset: [{
                column_data: [ ... ],
                column_name: str,
                column_type: str [continuous/categorical],
                column_datatype: str
            }]
            :return: a pandas Dataframe where each column is structured as expected
            :raises: DataException
        """
        data = self.dataset
        column_names = []
        categorical_columns = []
        numerical_columns = []
        unrecognized_columns = []
        data_structure = []
        for col in data:
            content = col.get("column_data", [])
            content_type = col.get("column_datatype", "object")
            column_name = col.get("column_name", "")
            column_type = col.get("column_type", "")
            data_structure.append(np.array(content, dtype=content_type))
            column_names.append(column_name)
            if column_type == NUMERICAL:
                numerical_columns.append(column_name)
            elif column_type == CATEGORICAL:
                categorical_columns.append(column_name)
            else:
                unrecognized_columns.append(column_name)

        # Transposing array. Since columns are appended row-wise, by transposing we obtain a column-wise data structure
        data_structure = np.array(data_structure)
        data_structure = np.moveaxis(data_structure,0,1)
        data_frame = pd.DataFrame(data=data_structure.tolist(), columns=column_names)

        if len(column_names) < 1:
            raise DataException("No column names are passed to the input data")

        self.dataframe = data_frame
        self.columns = column_names
        self.categorical_columns = categorical_columns
        self.continuous_columns = numerical_columns
        self.continuous_data = data_frame[numerical_columns]
        self.categorical_data = data_frame[categorical_columns]
        self.input_shape = str(data_structure.shape[1:])


    def categorize_column(self, col):
        if col in self.continuous_columns:
            return NUMERICAL
        if col in self.categorical_columns:
            return CATEGORICAL
        return OTHER


    def parse_tabular_data_json(self) -> list[dict]:
        """
        Converts data from a dataframe into a list of dictionaries
        :return: a dictionary in form of:
        dataset: [{
            column_data: [ ... ],
            column_name: str,
            column_type: str [numerical/categorical],
            column_datatype: str
        }]
        """
        return [
            {
                "column_data" : self.dataframe[col].to_numpy().tolist(),
                "column_name": col,
                "column_type": self.categorize_column(col),
                "column_datatype": str(self.dataframe[col].dtype)
            }
            for col in self.dataframe.columns
        ]


    def parse_data_to_registry(self) -> list[dict]:
        """
        Translates data structure from input coherence to a structured feature list
        :return:
        """
        feature_list = []
        for idx, col in enumerate(self.dataset):
            feat = {
                "feature_name": col.get("column_name", ""),
                "feature_position": idx,
                "is_categorical": True if col.get("column_type", "") == CATEGORICAL else False,
                "datatype": col.get("column_datatype", "")
            }
            feature_list.append(feat)
        return feature_list


    def get_data(self):
        return self.dataframe, self.columns, self.continuous_columns, self.categorical_columns


