from __future__ import annotations
from types import NoneType, UnionType

from typing import Annotated, Any, Literal, Union, get_args

from .errors import MissingArgument, MissingRequiredKey, InvalidType
from .item import Item, InternalItem
from .util import get_origin, pretty_type, generate_type_from_data

class _Missing:
    def __bool__(self) -> Literal[False]:
        return False

Missing = _Missing()

def validate(item: InternalItem, model: Model, value: Any, root_item: InternalItem | None = None, root_value: Any | _Missing = Missing) -> Any:
    root_item = root_item or item
    root_value = root_value or value

    if isinstance(item.ty, type) and issubclass(item.ty, Model):
        return item.ty(value)

    origin = get_origin(item.ty)

    if not isinstance(value, origin):
        raise InvalidType(f"{model.__class__.__name__}.{item.key} expected type {pretty_type(root_item)} but found {generate_type_from_data(root_value)}")

    if origin in [list, set, tuple]:
        internal_item = item.internal_items[0]

        list_output: list[InternalItem] = []

        for internal_value in value:
            list_output.append(validate(internal_item, model, internal_value, root_item, root_value))

        value = origin(list_output)

    elif origin is dict:
        internal_item_key, internal_item_value = item.internal_items

        dict_output: dict[Any, Any] = {}

        for internal_key, internal_value in value.items():
            internal_key = validate(internal_item_key, model, internal_key, root_item, root_value)
            internal_value = validate(internal_item_value, model, internal_value, root_item, root_value)

            dict_output[internal_key] = internal_value

        value = dict_output

    return value

def convert_to_item(cls: type, key: str, annotation: Any, existing: Item | None = None) -> Item:
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is Annotated:
        item = convert_to_item(cls, key, args[0], args[1])

    elif origin in (Union, UnionType):
        item = Item()
        item._key = key

        if args[1] is NoneType:
            item._default = lambda: None
            item._ty = (args[0], NoneType)
    else:
        item = Item(_key=key, _ty=annotation)

    if existing:
        for modified in existing._modified:
            setattr(item, modified, getattr(existing, modified))

    internal_items: list[InternalItem] = []

    for ty in get_args(annotation):
        internal_items.append(convert_to_item(cls, key, ty)._to_internal())

    item._internal_items = internal_items

    return item

class Model:
    _items: dict[str, InternalItem]

    def __init_subclass__(cls) -> None:
        items: dict[str, InternalItem] = {}

        for key, annotation in cls.__annotations__.items():
            item = convert_to_item(cls, key, annotation)._to_internal()
            items[item.actual_key] = item

        cls._items = items

    def __init__(self, data: dict[str, Any] | None = None, /, **kwargs: Any):
        if data is None and not kwargs:
            raise MissingArgument("No data or kwargs passed to Model")

        data = data or kwargs

        for key, item in self._items.items():
            if key not in data:
                if item.default:
                    setattr(self, item.key, item.default())
                else:
                    raise MissingRequiredKey(f"Missing required key {self.__class__.__name__}.{key}")

        for key, value in data.items():
            if not (item := self._items.get(key)):
                continue

            new_value = validate(item, self, value)

            setattr(self, item.key, new_value)

    def to_dict(self) -> dict[str, Any]:
        output: dict[str, Any] = {}

        for item in self._items.values():
            value = getattr(self, item.key)

            if isinstance(value, Model):
                value = value.to_dict()

            if isinstance(value, (list, set, tuple)):
                list_inner_output: list[Any] = []

                for inner_value in value:
                    if isinstance(inner_value, Model):
                        inner_value = inner_value.to_dict()

                    list_inner_output.append(inner_value)

                value: Any = type(value)(list_inner_output)

            if isinstance(value, dict):
                dict_inner_output: dict[Any, Any] = {}

                for inner_key, inner_value in value.items():
                    if isinstance(inner_value, Model):
                        inner_value = inner_value.to_dict()

                    dict_inner_output[inner_key] = inner_value

            output[item.actual_key] = value

        return output

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        items: list[str] = []

        for item in self._items.values():
            value = getattr(self, item.key)

            items.append(f"{item.key}={value!r}")

        return f"<{self.__class__.__name__} {' '.join(items)}>"
