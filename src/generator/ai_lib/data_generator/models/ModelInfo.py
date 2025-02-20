class AllowedData:
    def __init__(self, dtype:str, is_categorical:bool):
        self.dtype = dtype
        self.is_categorical = is_categorical

class ModelInfo:
    def __init__(self, name:str, default_loss_function:str, description:str, allowed_data:list[AllowedData]):
        self.name = name
        self.default_loss_function = default_loss_function
        self.description = description
        self.allowed_data = allowed_data

    def get_model_info(self):
        allowed_data = [
            {
                "data_type": ad.dtype,
                "is_categorical": ad.is_categorical
            } for ad in self.allowed_data
        ]
        system_model_info = {
            "name": self.name,
            "default_loss_function": self.default_loss_function,
            "description": self.description,
            "allowed_data": allowed_data
        }

        return system_model_info