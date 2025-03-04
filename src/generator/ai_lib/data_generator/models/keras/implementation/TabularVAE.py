import keras
from keras import layers

from ai_lib.Dataset import Dataset
from ai_lib.data_generator.models.ModelInfo import ModelInfo, AllowedData
from ai_lib.data_generator.models.keras.KerasBaseVAE import BaseKerasVAE, VAE
from ai_lib.preprocess.scale import standardize_input
from ai_lib.data_generator.models.keras.Sampling import Sampling


class TabularVAE(BaseKerasVAE):
    def __init__(
        self, metadata: dict, model_name: str, input_shape: str, load_path: str, latent_dim: int = 2
    ):
        super().__init__(metadata, model_name, input_shape, load_path, latent_dim)
        self._beta = 1
        self._learning_rate = 1e-3
        self._epochs = 200
        self._batch_size = 8
        self._instantiate()


    def _build(self, input_shape: tuple[int, ...]):
        encoder_inputs = keras.Input(shape=input_shape)
        x = layers.Dense(32, activation="relu")(encoder_inputs)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dense(16, activation="relu")(x)
        z_mean = layers.Dense(self._latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(self._latent_dim, name="z_log_var")(x)
        z = Sampling()([z_mean, z_log_var])
        encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

        latent_inputs = keras.Input(shape=(self._latent_dim,))
        y = layers.Dense(16, activation="relu")(latent_inputs)
        y = layers.Dense(64, activation="relu")(y)
        y = layers.Dense(32, activation="relu")(y)
        decoder_outputs = layers.Dense(input_shape[0], activation="linear")(y)
        decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")

        vae = VAE(encoder, decoder, self._beta)
        vae.summary()
        return vae

    def _pre_process(self, data: Dataset, **kwargs):
        cont_np_data = data.continuous_data.to_numpy()
        if not self._scaler:
            scaler, np_input_scaled, _ = standardize_input(train_data=cont_np_data)
            self._scaler = scaler
        else:
            np_input_scaled = self._scale(cont_np_data)
        return np_input_scaled


    @classmethod
    def self_describe(cls):
        return ModelInfo(
            name=f"{cls.__module__}.{cls.__qualname__}",
            default_loss_function="ELBO LOSS",
            description="A Variational Autoencoder for data generation",
            allowed_data=[
                AllowedData("float32", False),
                AllowedData("int32", False),
                AllowedData("int64", False),
            ],
        ).get_model_info()
