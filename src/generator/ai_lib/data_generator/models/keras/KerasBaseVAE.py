import pickle
from abc import ABC

import numpy as np
import os
import keras
from keras import saving, ops
import tensorflow as tf

from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from ai_lib.data_generator.models.TrainingInfo import TrainingInfo
from ai_lib.Dataset import Dataset

os.environ["KERAS_BACKEND"] = "tensorflow"


class BaseKerasVAE(UnspecializedModel, ABC):
    def __init__(
        self, metadata: dict, model_name: str, input_shape: str, load_path: str, latent_dim: int
    ):
        super().__init__(metadata, model_name, input_shape, load_path)
        self._latent_dim = latent_dim
        self._beta = None
        self._learning_rate = None
        self._batch_size = None
        self._epochs = None

    def _load(self, folder_path: str):
        encoder_filename = os.path.join(folder_path, "encoder.keras")
        decoder_filename = os.path.join(folder_path, "decoder.keras")
        scaler_filename = os.path.join(folder_path, "scaler.pkl")
        encoder = saving.load_model(encoder_filename)
        decoder = saving.load_model(decoder_filename)
        self._model = VAE(encoder, decoder, self._beta)

        with open(scaler_filename, "rb") as f:
            self._scaler = pickle.load(f)

    def _instantiate(self):
        if self._load_path is not None:
            self._load(self._load_path)
            return
        if not self._model and self._input_shape:
            self._model = self._build(self._input_shape)

    def save(self, folder_path: str):
        encoder_filename = os.path.join(folder_path, "encoder.keras")
        decoder_filename = os.path.join(folder_path, "decoder.keras")
        saving.save_model(self._model.encoder, encoder_filename)
        saving.save_model(self._model.decoder, decoder_filename)
        scaler_filename = os.path.join(folder_path, "scaler.pkl")

        with open(scaler_filename, "wb") as f:
            pickle.dump(self._scaler, f)

    def fine_tune(self, data: np.array, **kwargs):
        raise NotImplementedError

    def _build(self, input_shape: str):
        raise NotImplementedError

    def _scale(self, data: np.array):
        return self._scaler.transform(data)

    def _inverse_scale(self, data: np.array):
        return self._scaler.inverse_transform(data)

    def _pre_process(self, data: Dataset, **kwargs):
        raise NotImplementedError


    def train(self, data: Dataset):
        data = self._pre_process(data)
        self._model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self._learning_rate)
        )
        history = self._model.fit(
            data, epochs=self._epochs, batch_size=self._batch_size
        )
        self._training_info = TrainingInfo(
            loss_fn="ELBO",
            train_loss=history.history["loss"][-1].numpy().item(),
            train_samples=data.shape[0],
            validation_loss=-1,
            validation_samples=0,
        )

    def infer(self, n_rows: int, **kwargs):
        z_random = np.random.normal(size=(n_rows, self._latent_dim))
        results = self._model.decoder.predict(z_random)
        results = self._inverse_scale(results)
        return results

    @classmethod
    def self_describe(cls):
        raise NotImplementedError


class VAE(keras.Model):
    def __init__(self, encoder, decoder, beta=1, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self._beta = beta
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
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

            # TODO: Verify Working
            axes = tf.range(1, tf.rank(reconstruction))
            error = data - reconstruction
            reconstruction_loss = ops.mean(ops.square(error), axis=axes)
            # END TODO
            kl_loss = -0.5 * (1 + z_log_var - ops.square(z_mean) - ops.exp(z_log_var))
            kl_loss = ops.mean(ops.sum(kl_loss, axis=1))
            total_loss = reconstruction_loss + self._beta * kl_loss
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
