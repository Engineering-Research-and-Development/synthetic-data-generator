import builtins


class Parameter:
    def __init__(self, name:str, value:str, parameter_type:str):
        self.name = name
        self.value = value
        self.parameter_type = parameter_type

    def to_json(self):
        return {
            "name": self.name,
            "value": str(self.value),
            "parameter_type": self.parameter_type,
        }

    @classmethod
    def from_json(cls, json_data):
        target_type = getattr(builtins, json_data["parameter_type"])
        converted_value = target_type(json_data["value"])
        return cls(json_data["name"],
                   converted_value,
                   json_data["parameter_type"])
