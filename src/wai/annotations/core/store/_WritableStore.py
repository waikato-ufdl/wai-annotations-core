from abc import ABC, abstractmethod
from typing import Union

from ..util.path import FilePathLike
from ._Store import Store, StoreKeyType


class WritableStore(Store[StoreKeyType], ABC):
    """
    A store that data can be written to.
    """
    def write(self, key: Union[FilePathLike, str], data: bytes):
        """
        Writes an item to the store.

        :param key:
                    The key, either parsed or in its path representation.
        :param data:
                    The data to write.
        """
        return self._write(self.ensure_key(key), data)

    @abstractmethod
    def _write(self, key: StoreKeyType, data: bytes):
        """
        Writes an item to the store.

        :param key:
                    The key to access.
        :param data:
                    The data to store at the given key.
        """
        raise NotImplementedError(self._write.__qualname__)
