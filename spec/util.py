from __future__ import annotations

from typing import Any, Iterable, TypeGuard, get_origin as _get_origin, TYPE_CHECKING, Literal, Union
from types import UnionType

if TYPE_CHECKING:
    from .item import InternalItem

class _Missing:
    def __bool__(self) -> Literal[False]:
        return False

def is_union(ty: Any) -> bool:
    origin = get_origin(ty)

    return origin is Union or origin is UnionType

Missing = _Missing()

def get_origin(obj: Any) -> Any:
    return _get_origin(obj) or obj

def get_original_bases(obj: Any) -> tuple[Any, ...]:
    return getattr(obj, "__orig_bases__", ())

def pretty_type(item: InternalItem) -> str:
    if not isinstance(item.ty, list) and (generics := item.internal_items):
        generic_str = f"[{', '.join([pretty_type(generic) for generic in generics])}]"
    else:
        generic_str = ""

    return f"{item.ty.__name__ if not isinstance(item.ty, list) else to_union([ty.ty.__name__ for ty in item.ty])}{generic_str}"

def to_union(types: Iterable[Any]) -> str:
    return " | ".join(types or ["Unknown"])

def generate_type_from_data(data: Any) -> str:
    ty = type(data)

    if isinstance(data, (list, set, tuple)):
        types = set[Any]()

        for value in data:
            types.add(generate_type_from_data(value))

        generics = [to_union(types)]

    elif isinstance(data, dict):
        key_types = set[Any]()
        value_types = set[Any]()

        for key, value in data.items():
            key_types.add(generate_type_from_data(key))
            value_types.add(generate_type_from_data(value))

        generics = [to_union(key_types), to_union(value_types)]
    else:
        generics = []

    if generics:
        generic_str = f"[{', '.join(generics)}]"
    else:
        generic_str = ""

    return f"{ty.__name__}{generic_str}"
