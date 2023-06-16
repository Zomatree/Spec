from __future__ import annotations

from typing import Any, cast, get_origin as _get_origin, TYPE_CHECKING, Literal, Union
from types import UnionType
from typing_extensions import TypeVar

if TYPE_CHECKING:
    from .item import InternalItem

__all__ = ("UniqueList", "_Missing", "Missing", "is_union", "get_origin", "get_original_bases", "get_type_name", "pretty_type", "to_union", "generate_type_from_data")

T = TypeVar("T", default=Any)

class UniqueList(list[T]):
    def append(self, value: T):
        if value not in self:
            super().append(value)

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
    bases = getattr(obj, "__orig_bases__", ())

    assert isinstance(bases, tuple)

    return bases

def get_type_name(obj: Any) -> str:
    return cast(str, getattr(obj, "_type_name", obj.__name__))

def pretty_type(item: InternalItem) -> str:
    if not isinstance(item.ty, list) and (generics := item.internal_items):
        generic_str = f"[{', '.join([pretty_type(generic) for generic in generics])}]"
    else:
        generic_str = ""

    return f"{item.ty.__name__ if not isinstance(item.ty, list) else to_union([ty.ty.__name__ for ty in item.ty])}{generic_str}"

def to_union(types: list[Any]) -> str:
    return " | ".join(types or ["Unknown"])

def generate_type_from_data(data: Any) -> str:
    ty = type(data)

    if isinstance(data, (list, set, tuple)):
        types = UniqueList()

        for value in data:
            types.append(generate_type_from_data(value))

        generics = [to_union(types)]

    elif isinstance(data, dict):
        key_types = UniqueList()
        value_types = UniqueList()

        for key, value in data.items():
            key_types.append(generate_type_from_data(key))
            value_types.append(generate_type_from_data(value))

        generics = [to_union(key_types), to_union(value_types)]
    else:
        generics = []

    if generics:
        generic_str = f"[{', '.join(generics)}]"
    else:
        generic_str = ""

    return f"{ty.__name__}{generic_str}"
