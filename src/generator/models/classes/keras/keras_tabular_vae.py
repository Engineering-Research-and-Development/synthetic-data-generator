import numpy as np
import os
import keras
from keras import layers, saving, ops
from keras import initializers

import tensorflow as tf

from models.classes.Model import UnspecializedModel

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
        epsilon = keras.random.normal(shape=(batch, dim), seed=self.seed_generator)
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
            reconstruction_loss = ops.mean(ops.sum(keras.losses.mean_absolute_error(data, reconstruction)))
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

    def build(self, input_shape):
        latent_dim = 2

        encoder_inputs = keras.Input(shape=input_shape)
        x = layers.Dense(32, activation="relu")(encoder_inputs)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dense(16, activation="relu")(x)
        z_mean = layers.Dense(latent_dim, name="z_mean")(x)
        z_log_var = layers.Dense(latent_dim, kernel_initializer=initializers.zeros(),  name="z_log_var")(x)
        z = Sampling()([z_mean, z_log_var])
        encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

        latent_inputs = keras.Input(shape=(latent_dim,))
        y = layers.Dense(16, activation="relu")(latent_inputs)
        y = layers.Dense(64, activation="relu")(y)
        y = layers.Dense(32, activation="relu")(y)
        decoder_outputs = layers.Dense(input_shape[0], activation="relu")(y)
        decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")

        vae = VAE(encoder, decoder)
        vae.summary()
        return vae

    def load(self, weights_path):
        model = saving.load_model(weights_path)
        return model

    def train(self, data: np.array, **kwargs):
        self.model.compile(optimizer=keras.optimizers.Adam())
        history = self.model.fit(data, epochs=100, batch_size=1)
        self.metadata["training_info"] = {
            "loss": history.history["loss"][-1].numpy().item(),
            "val_loss": -1,
            "train_samples": data.shape[0],
            "validation_samples": 0
        }


    def fine_tune(self, data, **kwargs):
        pass

    def infer(self, n_rows, **kwargs):
        pass



