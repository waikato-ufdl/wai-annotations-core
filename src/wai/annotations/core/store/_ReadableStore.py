from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union

from ._Store import Store, StoreKeyType


class ReadableStore(Store[StoreKeyType]):
    """
    A store that data can be read from.
    """
    def read_exact(
            self,
            key: Union[StoreKeyType, str]
    ) -> Tuple[StoreKeyType, bytes]:
        """
        Reads exactly one item from the store.

        :param key:
                    A key, either parsed or in its string representation.
        :return:
                    The value stored at the given key.
        :raise Exception:

        """
        # If it is a specific key, just read it
        if not isinstance(key, str):
            return key, self.read(key)

        read = self.read_all(key)

        if len(read) == 0:
            raise Exception(f"Key '{key}' returned no data")
        elif len(read) > 1:
            raise Exception(f"Key '{key}' returned multiple results")

        return next(iter(read.items()))

    @abstractmethod
    def read_all(
            self,
            pattern: str,
            skip_data: bool = False
    ) -> Dict[StoreKeyType, bytes]:
        """
        Reads all items from the store that match a pattern. The interpretation of the
        pattern is store-specific.

        :param pattern:
                    The pattern to match.
        :param skip_data:
                    Whether to skip reading the file-data and just resolve the keys.
        :return:
                    A dictionary from all matching keys to their corresponding data
                    (or empty bytes if skip_data is True).
        """
        raise NotImplementedError(self.read_all.__qualname__)

    @abstractmethod
    def read(self, key: StoreKeyType) -> bytes:
        """
        Reads a specific item from the store.

        :param key:
                    A key to the store.
        :return:
                    The corresponding file-data.
        """
        raise NotImplementedError(self.read.__qualname__)
