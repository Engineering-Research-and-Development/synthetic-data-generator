import pickle

import numpy as np
import os
import keras
from keras import saving, ops
import tensorflow as tf

from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from ai_lib.data_generator.models.ModelInfo import ModelInfo, AllowedData
from ai_lib.data_generator.models.TrainingInfo import TrainingInfo
from ai_lib.Dataset import Dataset

os.environ["KERAS_BACKEND"] = "tensorflow"


class BaseKerasVAE(UnspecializedModel):
    def __init__(self, metadata: dict, model_name: str, input_shape: str, latent_dim: int = 2):
        super().__init__(metadata, model_name, input_shape)
        self.latent_dim = latent_dim
        self.scaler = None
        if not self.model and self.input_shape:
            self.model = self.build(self.input_shape)


    def load(self, folder_path: str):
        encoder_filename = os.path.join(folder_path, "encoder.keras")
        decoder_filename = os.path.join(folder_path, "decoder.keras")
        scaler_filename = os.path.join(folder_path, "scaler.pkl")
        encoder = saving.load_model(encoder_filename)
        decoder = saving.load_model(decoder_filename)
        self.model = VAE(encoder, decoder)

        with open(scaler_filename, "rb") as f:
            self.scaler = pickle.load(f)

    def save(self, folder_path: str, **kwargs):
        encoder_filename = os.path.join(folder_path, "encoder.keras")
        decoder_filename = os.path.join(folder_path, "decoder.keras")
        saving.save_model(self.model.encoder, encoder_filename)
        saving.save_model(self.model.decoder, decoder_filename)
        scaler_filename = os.path.join(folder_path, "scaler.pkl")

        with open(scaler_filename, 'wb') as f:
            pickle.dump(self.scaler, f)

    def fine_tune(self, data: np.array, **kwargs):
        pass

    def build(self, input_shape: str):
        pass

    def _scale(self, data: np.array):
        return self.scaler.transform(data)

    def _inverse_scale(self, data: np.array):
        return self.scaler.inverse_transform(data)

    def _pre_process(self, data: Dataset, **kwargs):
        return data

    def train(self, data: Dataset, **kwargs):
        data = self._pre_process(data)
        self.model.compile(optimizer=keras.optimizers.Adam(learning_rate=kwargs.get('learning_rate', 1e-3)))
        history = self.model.fit(data, epochs=kwargs.get('epochs', 200), batch_size=kwargs.get('batch_size', 8))
        self.training_info = TrainingInfo(
            loss_fn="ELBO",
            train_loss=history.history["loss"][-1].numpy().item(),
            train_samples=data.shape[0],
            validation_loss=-1,
            validation_samples=0
        )

    def infer(self, n_rows: int, **kwargs):
        z_random = np.random.normal(size=(n_rows, self.latent_dim))
        results = self.model.decoder.predict(z_random)
        return results

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
            ]
        ).get_model_info()


class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(name="reconstruction_loss")
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)
            reconstruction_loss = ops.mean(ops.sum(ops.abs(data - reconstruction), axis=-1))
            kl_loss = -0.5 * (1 + z_log_var - ops.square(z_mean) - ops.exp(z_log_var))
            kl_loss = ops.mean(ops.sum(kl_loss, axis=1))
            total_loss = reconstruction_loss + kl_loss
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)

        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }
