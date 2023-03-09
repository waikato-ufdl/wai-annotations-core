from typing import Type

from ..._LocalFileStore import LocalFileStore
from .._StoreSpecifier import StoreSpecifier


class LocalFileStoreSpecifier(StoreSpecifier[LocalFileStore]):
    """
    Specifies the local file store.
    """
    @classmethod
    def name(cls) -> str:
        return "Local file-system"

    @classmethod
    def description(cls) -> str:
        return "The file-system local to the current machine"

    @classmethod
    def store_type(cls) -> Type[LocalFileStore]:
        return LocalFileStore
