from abc import ABC, abstractmethod
from typing import Type, TypeVar, Hashable

from ...util.path import FilePathLike, PathKeyLike, path_to_str

SelfType = TypeVar('SelfType', bound='StoreKey')


class StoreKey(PathKeyLike, Hashable, ABC):
    """
    Base-type for store keys. Store-keys must be representable as
    though they were logically a path on the local filesystem. They
    must also be comparable for equality, and hashable.
    """
    @classmethod
    @abstractmethod
    def from_path(cls: Type[SelfType], path: FilePathLike) -> SelfType:
        """
        Parses a store-key from its path-like representation.

        :param path:
                    The path-like representation of the key.
        :return:
                    An instance of the store-key.
        """
        raise NotImplementedError(cls.from_path.__qualname__)

    @abstractmethod
    def __eq__(self, other):
        # Equality must be implemented to match __hash__
        raise NotImplementedError(self.__eq__.__qualname__)

    @property
    def path(self) -> str:
        """
        Returns the path representation of the key.
        """
        return path_to_str(self)

    def __str__(self) -> str:
        return f"{type(self).__name__} '{self.path}'"

