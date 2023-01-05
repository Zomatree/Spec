from __future__ import annotations

from dataclasses import dataclass, field

from typing import Callable, Any, Generic, Self
from typing_extensions import TypeVar

__all__ = ("Item", "InternalItem", "rename", "default", "validate", "hook")

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

    def _to_internal(self) -> InternalItem[T]:
        assert self._key
        assert self._ty

        return InternalItem(self._key, self._rename, self._ty, self._internal_items or [], self._default, self._validate, self._hook)

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

@dataclass
class InternalItem(Generic[T]):
    key: str
    rename: str | None
    ty: type[T]
    internal_items: list[InternalItem]
    default: Callable[[], T] | None = None
    validate: Callable[[T], bool] = lambda _: True
    hook: Callable[[T], T] = lambda x: x

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
