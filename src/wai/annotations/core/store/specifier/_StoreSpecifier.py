from abc import abstractmethod
from typing import Type, TypeVar, Generic

from ...plugin.specifier import PluginSpecifier
from .._ReadableStore import ReadableStore
from .._WritableStore import WritableStore
from .._Store import Store

StoreType = TypeVar('StoreType', bound=Store)


class StoreSpecifier(PluginSpecifier, Generic[StoreType]):
    """
    Class which specifies a type of store available for use by wai.annotations.
    """
    @classmethod
    @abstractmethod
    def store_type(cls) -> Type[StoreType]:
        """
        The type of the store.
        """
        raise NotImplementedError(cls.store_type.__qualname__)

    @classmethod
    def is_readable(cls) -> bool:
        return issubclass(cls.store_type(), ReadableStore)

    @classmethod
    def is_writable(cls) -> bool:
        return issubclass(cls.store_type(), WritableStore)
