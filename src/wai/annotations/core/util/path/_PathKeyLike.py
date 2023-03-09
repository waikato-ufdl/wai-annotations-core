from abc import abstractmethod
from typing import TYPE_CHECKING

from ._FilePathLike import FilePathLike
from ._FilePath import FilePath

if TYPE_CHECKING:
    from ._PathKey import PathKey


class PathKeyLike(FilePathLike):
    """
    Interface representing something that can be converted to a PathKey.
    """
    @abstractmethod
    def as_path_key(self) -> 'PathKey':
        """
        Gets a path-key representation of this object.
        """
        raise NotImplementedError(self.as_path_key.__qualname__)

    def as_file_path(self) -> FilePath:
        return self.as_path_key()
