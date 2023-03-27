__all__ = ("SpecError", "MissingArgument", "MissingRequiredKey", "InvalidType")

class SpecError(Exception):
    def __init__(self, model_name: str, message: str) -> None:
        self.model_name = model_name
        self.message = message
        super().__init__(message)

    def to_dict(self):
        return {"model_name": self.model_name, "message": self.message}

class MissingArgument(SpecError):
    def __init__(self, model_name: str):
        super().__init__(model_name, "No data or kwargs passed to Model")

class MissingRequiredKey(SpecError):
    def __init__(self, model_name: str, key: str):
        self.key = key
        super().__init__(model_name, f"Missing required key {model_name}.{key}")

    def to_dict(self):
        return super().to_dict() | {"key": self.key}

class InvalidType(SpecError):
    def __init__(self, model_name: str, key: str, expected: str, ty: str) -> None:
        self.key = key
        self.expected = expected
        self.ty = ty
        super().__init__(model_name, f"{model_name}.{key} expected type {expected} but found {ty}")

    def to_dict(self):
        return super().to_dict() | {"key": self.key, "expected": self.expected, "ty": self.ty}

class FailedValidation(SpecError):
    def __init__(self, model_name: str, key: str) -> None:
        self.key = key
        super().__init__(model_name, f"{model_name}.{key} failed validation")

    def to_dict(self):
        return super().to_dict() | {"key": self.key}

class UnknownUnionKey(SpecError):
    def __init__(self, model_name: str, key: str) -> None:
        self.key = key
        super().__init__(model_name, f"Unknown key found `{key}`")

    def to_dict(self):
        return super().to_dict() | {"key": self.key}

class MissingTypeName(SpecError):
    def __init__(self, model_name: str, key: str, ty: str) -> None:
        self.key = key
        self.ty = ty
        super().__init__(model_name, f"{model_name}.{key} union type is missing a type name for {ty}")

    def to_dict(self):
        return super().to_dict() | {"key": self.key, "ty": self.ty}

class SpecErrorGroup(ExceptionGroup):
    exceptions: list[SpecError]

    def to_dict(self):
        return {"message": self.message, "errors": [e.to_dict() for e in self.exceptions]}
