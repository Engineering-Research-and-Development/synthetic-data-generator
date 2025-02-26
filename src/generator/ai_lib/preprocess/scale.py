from sklearn.preprocessing import StandardScaler
import numpy as np


def standardize_input(
    train_data: np.array, test_data: np.array = None
) -> tuple[np.array, np.array, StandardScaler]:
    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data)
    if test_data is not None:
        test_data = scaler.transform(test_data)

    return scaler, train_data, test_data


def standardize_time_series(
    train_data: np.array, test_data: np.array = None
) -> tuple[np.array, np.array, StandardScaler]:
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
