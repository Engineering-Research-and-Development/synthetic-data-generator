class Parameter:
    def __init__(self, name, value, parameter_type):
        self.name = name
        self.value = value
        self.parameter_type = parameter_type

    def to_json(self):
        return {
            "name": self.name,
            "value": self.value,
            "parameter_type": self.parameter_type,
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data["name"], json_data["value"], json_data["parameter_type"])
