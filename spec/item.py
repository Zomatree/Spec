from __future__ import annotations

from dataclasses import dataclass, field

from typing import Callable, Any, Generic, Self
from typing_extensions import TypeVar

__all__ = ("Item", "InternalItem", "rename", "default")

T = TypeVar("T", default=Any)

@dataclass
class Item(Generic[T]):
    _key: str | None = None
    _rename: str | None = None
    _ty: type[T] | None = None
    _internal_items: list[InternalItem] | None = None
    _default: Callable[[], T] | None = None
    _modified: list[str] = field(default_factory=lambda: [])

    def _to_internal(self) -> InternalItem[T]:
        assert self._key
        assert self._ty

        return InternalItem(self._key, self._rename, self._ty, self._internal_items or [], self._default)

    def rename(self, key: str) -> Self:
        self._rename = key
        self._modified.append("_rename")

        return self

    def default(self, default: Callable[[], T]) -> Self:
        self._default = default
        self._modified.append("_default")

        return self

@dataclass
class InternalItem(Generic[T]):
    key: str
    rename: str | None
    ty: type[T]
    internal_items: list[InternalItem]
    default: Callable[[], T] | None = None

    @property
    def actual_key(self) -> str:
        return self.rename or self.key

def rename(key: str) -> Item:
    return Item().rename(key)

def default(default: Callable[[], T]) -> Item[T]:
    return Item().default(default)
