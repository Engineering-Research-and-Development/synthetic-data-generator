def trim_name(elem: str):
    first_occ = elem.rfind(".")
    return elem[first_occ + 1 :]


def format_training_info(tr_info: dict):
    payload = {
        "loss_function": tr_info["loss_fn"],
        "train_loss": tr_info["train_loss"],
        "val_loss": tr_info["validation_loss"],
        "train_samples": tr_info["train_samples"],
        "val_samples": tr_info["validation_samples"],
    }
    return payload
