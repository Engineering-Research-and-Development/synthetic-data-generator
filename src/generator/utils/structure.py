import os

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
