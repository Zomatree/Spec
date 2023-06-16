__all__ = ("SpecError", "MissingArgument", "MissingRequiredKey", "InvalidType", "FailedValidation", "UnknownUnionKey", "MissingTypeName")

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

class UnknownUnionKey(SpecError):
    pass

class MissingTypeName(SpecError):
    pass
