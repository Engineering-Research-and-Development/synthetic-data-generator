from models.model_factory import model_factory
import pandas as pd
import os

from utils.structure import MODEL_FOLDER

if __name__ == "__main__":

    model_folder = os.path.join(MODEL_FOLDER, "Test-T_VAE:1")
    test = {
        "image": model_folder,
        "model_name": "Test-T_VAE",
        "algorithm": "models.classes.keras.keras_tabular_vae.KerasTabularVAE",
        "metadata": {
            "input_shape": "(13)",
            "model_version": "v1"
        }
    }
    m = model_factory(test)
    print(m)
    print(m.scaler)
    print(m.metadata)
    new_data = m.infer(1000)
    df_predict = pd.DataFrame(m.scaler.inverse_transform(new_data))
    df_predict.to_csv("wine_generated_infer.csv", index=False)
    df_predict.describe()