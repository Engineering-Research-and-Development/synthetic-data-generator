from sklearn.preprocessing import StandardScaler
import numpy as np

from ai_lib.Exceptions import DataException


def standardize_simple_tabular_input(
    train_data: np.array, test_data: np.array = None
) -> tuple[StandardScaler, np.array, np.array]:

    if len(train_data.shape) != 2:
        raise DataException("Data must be in the format (batch, features)")

    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data)
    if test_data is not None:
        test_data = scaler.transform(test_data)

    return scaler, train_data, test_data


def standardize_simple_tabular_time_series(
    train_data: np.array, test_data: np.array = None
) -> tuple[StandardScaler, np.array, np.array]:
    scaler = StandardScaler()

    if len(train_data.shape) != 3:
        raise DataException("Data must be in the format (batch, features, steps)")

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
