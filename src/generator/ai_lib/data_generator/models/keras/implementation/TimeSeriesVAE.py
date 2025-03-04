import numpy as np
import keras

from ai_lib.Dataset import Dataset
from ai_lib.data_generator.models.ModelInfo import ModelInfo, AllowedData
from ai_lib.data_generator.models.keras.KerasBaseVAE import BaseKerasVAE, VAE
from keras import layers

from ai_lib.preprocess.scale import standardize_time_series
from ai_lib.data_generator.models.keras.Sampling import Sampling


class TimeSeriesVAE(BaseKerasVAE):
    def __init__(
        self, metadata: dict, model_name: str, input_shape: str, load_path: str, latent_dim: int = 6
    ):
        super().__init__(metadata, model_name, input_shape, load_path, latent_dim)
        self._beta = 0.15
        self._learning_rate = 3e-3
        self._epochs = 100
        self._batch_size = 16

        if not self._model and self._input_shape:
            self._model = self._build(self._input_shape)
        if self._load_path is not None:
            self._load(self._load_path)

    def _build(self, input_shape: tuple[int, ...]):
        encoder_inputs = keras.Input(shape=input_shape)
        encoder_inputs = layers.Permute((1, 2))(encoder_inputs)
        x = layers.Conv1D(32, 3, activation="relu", strides=2, padding="same")(
            encoder_inputs
        )
        x = layers.Conv1D(64, 3, activation="relu", strides=2, padding="same")(x)
        x = layers.Flatten()(x)
        x = layers.Dense(16, activation="relu")(x)
        z_mean = layers.Dense(self._latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(self._latent_dim, name="z_log_var")(x)
        z = Sampling()([z_mean, z_log_var])
        encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

        shape_out = int(np.round(input_shape[1] / 4, 0))
        latent_inputs = keras.Input(shape=(self._latent_dim,))
        y = layers.Dense(shape_out * 64, activation="relu")(latent_inputs)
        y = layers.Reshape((shape_out, 64))(y)
        y = layers.Conv1DTranspose(64, 3, activation="relu", strides=2, padding="same")(
            y
        )
        y = layers.Conv1DTranspose(32, 3, activation="relu", strides=2, padding="same")(
            y
        )
        decoder_outputs = layers.Conv1DTranspose(
            input_shape[0], 3, activation="relu", padding="same"
        )(y)
        decoder_outputs = layers.Permute((2, 1))(decoder_outputs)
        decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")

        vae = VAE(encoder, decoder, self._beta)
        vae.summary()
        return vae

    def _scale(self, data: np.array):
        batch, feats, steps = data.shape
        return self._scaler.transform(data.reshape(-1, feats * steps)).reshape(
            -1, feats, steps
        )

    def _inverse_scale(self, data: np.array):
        batch, feats, steps = data.shape
        return self._scaler.inverse_transform(data.reshape(-1, feats * steps)).reshape(
            -1, feats, steps
        )

    def _pre_process(self, data: Dataset, **kwargs):
        np_data = np.array(data.dataframe.values.tolist())
        if not self._scaler:
            scaler, np_input_scaled, _ = standardize_time_series(train_data=np_data)
            self._scaler = scaler
        else:
            np_input_scaled = self._scale(np_data)
        return np_input_scaled

    @classmethod
    def self_describe(cls):
        return ModelInfo(
            name=f"{cls.__module__}.{cls.__qualname__}",
            default_loss_function="ELBO LOSS",
            description="A Beta-Variational Autoencoder for time series generation",
            allowed_data=[
                AllowedData("float32", False),
                AllowedData("int32", False),
                AllowedData("int64", False),
            ],
        ).get_model_info()
