import datetime
import pickle

import numpy as np
import os
import keras
from keras import layers, saving, ops
from keras import initializers
import tensorflow as tf

from models.classes.Model import UnspecializedModel
from utils.structure import MODEL_FOLDER

os.environ["KERAS_BACKEND"] = "tensorflow"


class Sampling(layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seed_generator = keras.random.SeedGenerator(42)

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = ops.shape(z_mean)[0]
        dim = ops.shape(z_mean)[1]
        epsilon = keras.random.uniform(shape=(batch, dim), seed=self.seed_generator)
        return z_mean + ops.exp(0.5 * z_log_var) * epsilon


class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
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



class KerasTabularVAE(UnspecializedModel):

    def __init__(self, metadata:dict, model_name:str, model_filepath:str=None):
        super().__init__(metadata, model_name, model_filepath)
        self.latent_dim = 2


    def build(self, input_shape:tuple[int,...]):
        encoder_inputs = keras.Input(shape=input_shape)
        x = layers.Dense(32, activation="relu")(encoder_inputs)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dense(16, activation="relu")(x)
        z_mean = layers.Dense(self.latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(self.latent_dim,  name="z_log_var")(x)
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


    def load(self):
        encoder_filename = os.path.join(self.model_filepath, "encoder.keras")
        decoder_filename = os.path.join(self.model_filepath, "decoder.keras")
        scaler_filename = os.path.join(self.model_filepath, "scaler.pkl")
        encoder = saving.load_model(encoder_filename)
        decoder = saving.load_model(decoder_filename)
        model = VAE(encoder, decoder)
        with open(scaler_filename, "rb") as f:
            scaler = pickle.load(f)
        return model, scaler


    def train(self, data: np.array, **kwargs):
        self.model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3))
        history = self.model.fit(data, epochs=200, batch_size=8)
        self.metadata["training_info"] = {
            "loss_name": "ELBO",
            "train_loss": history.history["loss"][-1].numpy().item(),
            "val_loss": -1,
            "train_samples": data.shape[0],
            "validation_samples": 0
        }


    def fine_tune(self, data: np.array, **kwargs):
        pass


    def infer(self, n_rows:int, **kwargs):
        z_random = np.random.normal(size=(n_rows, self.latent_dim))
        results = self.model.decoder.predict(z_random)
        return results


    def save(self, **kwargs):
        new_version = self.check_folder_latest_version() + 1
        model_folder = f"{self.model_name}:{new_version}"
        save_folder = os.path.join(MODEL_FOLDER, model_folder)

        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        try:
            encoder_filename = os.path.join(save_folder, "encoder.keras")
            decoder_filename = os.path.join(save_folder, "decoder.keras")
            saving.save_model(self.model.encoder, encoder_filename)
            saving.save_model(self.model.decoder, decoder_filename)
        except Exception as e:
            print("Unable to save the model file", e)
            return

        try:
            scaler_filename = os.path.join(save_folder, "scaler.pkl")
            with open(scaler_filename, 'wb') as f:
                pickle.dump(self.scaler, f)
        except Exception as e:
            print("Unable to save the scaler file", e)
            return

        self.model_filepath = save_folder


    @classmethod
    def self_describe(cls):
        # Returns a dictionary with model info, useful for initializing model

        system_model_info = {
            "name": f"{cls.__module__}.{cls.__qualname__}",
            "default_loss_function": "ELBO Loss",
            "description": "A Tabular Variational Autoencoder for continuous numerical data generation",
            "data_types":  [
                {
                    "data_type": "float",
                    "is_categorical": False
                },
                {
                    "data_type": "int",
                    "is_categorical": False
                },
            ]
        }

        return system_model_info



