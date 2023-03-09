from typing import Type

from ._StoreKey import StoreKey
from ...util.path import FilePathLike, PathKey, path_to_str


class BasicStoreKey(StoreKey):
    """
    A store-key type which only wraps a PathKey.
    """
    def __init__(self, path: str):
        self._path_key = PathKey(path)

    def as_path_key(self) -> PathKey:
        return self._path_key

    def __eq__(self, other):
        if isinstance(other, BasicStoreKey):
            other = other._path_key
        return isinstance(other, PathKey) and other == self._path_key

    def __hash__(self):
        return hash(self._path_key)

    @classmethod
    def from_path(cls: Type['BasicStoreKey'], path: FilePathLike) -> 'BasicStoreKey':
        return BasicStoreKey(path_to_str(path))
