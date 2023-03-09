from abc import abstractmethod
from os import PathLike
from typing import TYPE_CHECKING

from ._path_to_str import path_to_str

if TYPE_CHECKING:
    from ._FilePath import FilePath


class FilePathLike(PathLike):
    """
    Interface representing something that can be converted to a FilePath.
    """
    @abstractmethod
    def as_file_path(self) -> 'FilePath':
        """
        Gets a file-path representation of this object.
        """
        raise NotImplementedError(self.as_file_path.__qualname__)

    def __fspath__(self) -> str:
        # Default implementation is to convert self -> FilePath -> str
        return path_to_str(self.as_file_path())

    @classmethod
    def __subclasshook__(cls, subclass):
        return NotImplemented
