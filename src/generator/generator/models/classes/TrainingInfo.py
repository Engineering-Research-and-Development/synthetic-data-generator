class TrainingInfo:
    def __init__(
        self,
        loss_fn: str,
        train_samples: int,
        train_loss: float,
        validation_samples: int = None,
        validation_loss: int = None,
    ):
        self.loss_fn = loss_fn
        self.train_samples = train_samples
        self.train_loss = train_loss
        self.validation_samples = validation_samples
        self.validation_loss = validation_loss
