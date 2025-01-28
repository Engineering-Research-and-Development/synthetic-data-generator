"""Custom errors so that the service layer can work outside FASTApi context"""
class ValidationError(Exception):
    def __init__(self, message):
        # Calling the base class constructor with the parameters it needs
        super().__init__(message)

class NoVersions(Exception):
    def __init__(self, message):
        # Calling the base class constructor with the parameters it needs
        super().__init__(message)

class NoModelFound(Exception):
    def __init__(self, message):
        # Calling the base class constructor with the parameters it needs
        super().__init__(message)

class VersionNotFound(Exception):
    def __init__(self, message):
        # Calling the base class constructor with the parameters it needs
        super().__init__(message)