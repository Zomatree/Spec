__all__ = ("SpecError", "MissingArgument", "MissingRequiredKey", "InvalidType")

class SpecError(Exception):
    pass

class MissingArgument(SpecError):
    pass

class MissingRequiredKey(SpecError):
    pass

class InvalidType(SpecError):
    pass

class FailedValidation(SpecError):
    pass
