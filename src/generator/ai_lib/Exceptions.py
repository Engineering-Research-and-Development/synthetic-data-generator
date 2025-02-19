class DataException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ModelException(Exception):
    def __init__(self, message):
        super().__init__(message)
