from server.utilities import trim_name, format_training_info


def test_trim_name():
    assert trim_name("model.version.1") == "1"
    assert trim_name("data.file.csv") == "csv"
    assert trim_name("no_extension") == "no_extension"
    assert trim_name(".hiddenfile") == "hiddenfile"


def test_format_training_info():
    training_data = {
        "loss_fn": "mse",
        "train_loss": 0.02,
        "validation_loss": 0.03,
        "train_samples": 1000,
        "validation_samples": 200,
    }
    formatted_info = format_training_info(training_data)

    assert formatted_info["loss_function"] == "mse"
    assert formatted_info["train_loss"] == 0.02
    assert formatted_info["val_loss"] == 0.03
    assert formatted_info["train_samples"] == 1000
    assert formatted_info["val_samples"] == 200
