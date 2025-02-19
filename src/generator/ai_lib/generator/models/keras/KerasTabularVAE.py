import keras
from keras import layers

from ai_lib.Dataset import Dataset
from .BaseVAE import BaseVAE, VAE
from ai_lib.preprocess.scale import standardize_input
from .Sampling import Sampling


class KerasTabularVAE(BaseVAE):
    def __init__(self, metadata: dict, model_name: str, input_shape: str = "", model_filepath: str = None, latent_dim: int = 2):
        super().__init__(metadata, model_name, input_shape, model_filepath, latent_dim)

    def build(self, input_shape: tuple[int, ...]):
        encoder_inputs = keras.Input(shape=input_shape)
        x = layers.Dense(32, activation="relu")(encoder_inputs)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dense(16, activation="relu")(x)
        z_mean = layers.Dense(self.latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(self.latent_dim, name="z_log_var")(x)
        z = Sampling()([z_mean, z_log_var])
        encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

        latent_inputs = keras.Input(shape=(self.latent_dim,))
        y = layers.Dense(16, activation="relu")(latent_inputs)
        y = layers.Dense(64, activation="relu")(y)
        y = layers.Dense(32, activation="relu")(y)
        decoder_outputs = layers.Dense(input_shape[0], activation="linear")(y)
        decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")

        vae = VAE(encoder, decoder)
        vae.summary()
        return vae

    def pre_process(self, data: Dataset, **kwargs):
        cont_np_data = data.continuous_data.to_numpy()
        if not self.scaler:
            scaler, np_input_scaled, _ = standardize_input(train_data=cont_np_data)
            self.scaler = scaler
        else:
            np_input_scaled = self.scale(cont_np_data)
        return np_input_scaled