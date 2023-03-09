from typing import Type

from ..._DictStore import DictStore
from .._StoreSpecifier import StoreSpecifier


class DictStoreSpecifier(StoreSpecifier[DictStore]):
    """
    Specifies the dict store.
    """
    @classmethod
    def name(cls) -> str:
        return "Dict-store"

    @classmethod
    def description(cls) -> str:
        return "An in-memory dictionary store"

    @classmethod
    def store_type(cls) -> Type[DictStore]:
        return DictStore
