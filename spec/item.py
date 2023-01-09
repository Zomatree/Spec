from __future__ import annotations

from dataclasses import dataclass, field

from typing import Callable, Any, Generic, Literal, Self, overload
from typing_extensions import TypeVar

__all__ = ("Item", "InternalItem", "rename", "default", "validate", "hook", "tag")

T = TypeVar("T", default=Any)

@dataclass
class Item(Generic[T]):
    _key: str | None = None
    _rename: str | None = None
    _ty: type[T] | None = None
    _internal_items: list[InternalItem] | None = None
    _default: Callable[[], T] | None = None
    _modified: list[str] = field(default_factory=lambda: [])
    _validate: Callable[[T], bool] = lambda _: True
    _hook: Callable[[T], T] = lambda x: x
    _tag: Literal["untagged", "external", "internal", "ajacent"] = "untagged"
    _tag_info: dict[str, Any] = field(default_factory=lambda: {})
    _type_name: str | None = None

    def _to_internal(self) -> InternalItem[T]:
        assert self._key is not None
        assert self._ty is not None

        return InternalItem(self._key, self._rename, self._ty, self._internal_items or [], self._default, self._validate, self._hook, self._tag, self._tag_info, self._type_name)

    def rename(self, key: str) -> Self:
        self._rename = key
        self._modified.append("_rename")

        return self

    def default(self, default: Callable[[], T]) -> Self:
        self._default = default
        self._modified.append("_default")

        return self

    def validate(self, validator: Callable[[T], bool]) -> Self:
        self._validate = validator
        self._modified.append("_validate")

        return self

    def hook(self, f: Callable[[T], T]) -> Self:
        self._hook = f
        self._modified.append("_hook")

        return self

    @overload
    def tag(self, tag_type: Literal["untagged"]) -> Self:
        ...

    @overload
    def tag(self, tag_type: Literal["external"]) -> Self:
        ...

    @overload
    def tag(self, tag_type: Literal["internal"], *, tag: Any) -> Self:
        ...

    @overload
    def tag(self, tag_type: Literal["ajacent"], *, tag: Any, content: Any) -> Self:
        ...

    def tag(self, tag_type: Literal["untagged", "external", "internal", "ajacent"], **kwargs: Any) -> Self:
        self._tag = tag_type
        self._tag_info = kwargs

        self._modified.extend(["_tag", "_tag_info"])

        return self

    def type_name(self, name: str) -> Self:
        self._type_name = name
        self._modified.append("_type_name")

        return self

@dataclass
class InternalItem(Generic[T]):
    key: str
    rename: str | None
    ty: type[T]
    internal_items: list[InternalItem]
    default: Callable[[], T] | None
    validate: Callable[[T], bool]
    hook: Callable[[T], T]
    tag: Literal["untagged", "external", "internal", "ajacent"]
    tag_info: dict[str, Any]
    type_name: str | None

    @property
    def actual_key(self) -> str:
        return self.rename or self.key


def rename(key: str) -> Item:
    return Item().rename(key)

def default(default: Callable[[], T]) -> Item[T]:
    return Item().default(default)

def validate(validator: Callable[[T], bool]) -> Item[T]:
    return Item().validate(validator)

def hook(f: Callable[[T], T]) -> Item[T]:
    return Item().hook(f)

@overload
def tag(tag_type: Literal["untagged"]) -> Item[T]:
    ...

@overload
def tag(tag_type: Literal["external"]) -> Item[T]:
    ...

@overload
def tag(tag_type: Literal["internal"], *, tag: Any) -> Item[T]:
    ...

@overload
def tag(tag_type: Literal["ajacent"], *, tag: Any, content: Any) -> Item[T]:
    ...

def tag(tag_type: Literal["untagged", "external", "internal", "ajacent"], **kwargs: Any) -> Item[T]:
    return Item().tag(tag_type, **kwargs)
