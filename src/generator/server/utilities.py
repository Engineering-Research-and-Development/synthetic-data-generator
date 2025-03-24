from ai_lib.browse_algorithms import browse_algorithms
from server.file_utils import APP_FOLDER
from server.middleware_handlers import sync_remote_trained, generator_algorithms, sync_remote_algorithm


def trim_name(elem: str):
    first_occ = elem.rfind(".")
    return elem[first_occ + 1 :]


def server_startup():
    sync_remote_trained("trained_models/image-paths/", APP_FOLDER)
    [generator_algorithms.append(algorithm) for algorithm in browse_algorithms()]
    sync_remote_algorithm()


def format_training_info(tr_info: dict):
    payload = {
        "loss_function": tr_info["loss_fn"],
        "train_loss": tr_info["train_loss"],
        "val_loss": tr_info["validation_loss"],
        "train_samples": tr_info["train_samples"],
        "val_samples": tr_info["validation_samples"],
    }
    return payload
