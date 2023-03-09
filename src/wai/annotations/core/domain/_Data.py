from abc import abstractmethod
from typing import Type, TypeVar
from ..logging import LoggingEnabled, get_library_root_logger


SelfType = TypeVar('SelfType', bound="Data")


class Data(LoggingEnabled):
    """
    The base class for the independent data-type of items in a data-set
    of a particular domain. Should be sub-typed by specific domains
    to represent items in that domain, e.g. image files for image-based domains.
    The only guarantees of the base-type is that the data-type has a binary
    representation, and it can be instantiated from just that representation.
    """
    def __init__(self, data: bytes):
        self._data: bytes = data

    @property
    def data(self) -> bytes:
        """
        The binary contents of the file, if available.
        """
        return self._data

    @classmethod
    @abstractmethod
    def from_data(cls: Type[SelfType], file_data: bytes) -> SelfType:
        """
        Creates an instance of this type from just the binary file data.

        :param file_data:   The file-data.
        :return:            A FileInfo instance.
        """
        raise NotImplementedError(cls.from_data.__qualname__)
