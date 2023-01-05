from typing import Any, get_origin as _get_origin

__all__ = ("get_origin",)

def get_origin(obj: Any) -> Any:
    return _get_origin(obj) or obj
