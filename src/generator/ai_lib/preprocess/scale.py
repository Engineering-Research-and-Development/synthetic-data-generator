from sklearn.preprocessing import StandardScaler
import numpy as np


def standardize_simple_tabular_input(
    train_data: np.array, test_data: np.array = None
) -> tuple[StandardScaler, np.array, np.array]:
    """
    Standardizes the tabular input data by scaling features to have zero mean and unit variance.

    :param train_data: A numpy array of shape (batch, features) representing the training data.
    :param test_data: An optional numpy array of shape (batch, features) representing the test data.
    :return: A tuple containing the fitted StandardScaler, the standardized training data, and the standardized test data
             if provided.
    :raises DataException: If the input data does not have the expected shape.
    """

    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data)
    if test_data is not None:
        test_data = scaler.transform(test_data)

    return scaler, train_data, test_data


def standardize_simple_tabular_time_series(
    train_data: np.array, test_data: np.array = None
) -> tuple[StandardScaler, np.array, np.array]:
    """
    Standardizes the time series data by scaling features to have zero mean and unit variance.

    :param train_data: A numpy array of shape (batch, features, steps) representing the training data.
    :param test_data: An optional numpy array of shape (batch, features, steps) representing the test data.
    :return: A tuple containing the fitted StandardScaler, the standardized training data, and the standardized test data
             if provided.
    :raises DataException: If the input data does not have the expected shape.
    """
    scaler = StandardScaler()

    batch, features, steps = train_data.shape
    train_data = train_data.reshape(-1, features * steps)

    train_data = scaler.fit_transform(train_data.reshape(-1, features * steps)).reshape(
        -1, features, steps
    )

    if test_data is not None:
        test_data = scaler.transform(test_data.reshape(-1, features * steps)).reshape(
            -1, features, steps
        )

    return scaler, train_data, test_data
