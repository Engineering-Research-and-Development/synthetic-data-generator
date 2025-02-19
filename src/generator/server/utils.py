import json
import os
import pandas as pd

ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, "outputs")
MODEL_FOLDER = os.path.join(OUTPUT_FOLDER, "models")
GENERATION_FOLDER = os.path.join(OUTPUT_FOLDER, "datasets")


def create_folder_structure():
    if not os.path.isdir(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    if not os.path.isdir(MODEL_FOLDER):
        os.mkdir(MODEL_FOLDER)
    if not os.path.isdir(GENERATION_FOLDER):
        os.mkdir(GENERATION_FOLDER)


def store_files(gen_name: str, dataset: pd.DataFrame, metrics: dict):
    dir_path = os.path.join(GENERATION_FOLDER, gen_name)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    dataset_path = os.path.join(dir_path, "generation.csv")
    report_path = os.path.join(dir_path, "report.json")

    dataset.to_csv(dataset_path)

    if metrics is not None:
        with open(report_path, "w") as f:
            json.dump(metrics, f, indent=6)
