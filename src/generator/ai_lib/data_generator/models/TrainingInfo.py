import json


class TrainingInfo:
    def __init__(
        self,
        loss_fn: str,
        train_samples: int,
        train_loss: float,
        validation_samples: int = None,
        validation_loss: float = None,
    ):
        self._loss_fn = loss_fn
        self._train_samples = train_samples
        self._train_loss = train_loss
        self._validation_samples = validation_samples
        self._validation_loss = validation_loss

    def to_dict(self) -> dict:
        return {
            "loss_fn": self._loss_fn,
            "train_samples": self._train_samples,
            "train_loss": self._train_loss,
            "validation_samples": self._validation_samples,
            "validation_loss": self._validation_loss,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
