from abc import abstractmethod
from typing import Generic, Type, TypeVar, Union

from wai.common.cli import CLIInstantiable
from wai.common.meta.code_repr import (
    CodeRepresentable,
    CodeRepresentation,
    ImportDict,
    get_import_dict,
    code_repr
)

from ..util.path import FilePath, FilePathLike
from .key import StoreKey

StoreKeyType = TypeVar('StoreKeyType', bound=StoreKey)


class Store(
    CodeRepresentable,
    CLIInstantiable,
    Generic[StoreKeyType]
):
    """
    A generalised store of information. This is a key-value store where the
    keys are objects that implement the StoreKey interface and the values are
    blobs of binary data.
    """
    @abstractmethod
    def store_key_type(self) -> Type[StoreKeyType]:
        """
        Gets the type of the store-key.
        """
        raise NotImplementedError(self.store_key_type.__qualname__)

    def ensure_key(self, key: Union[FilePathLike, str]) -> StoreKeyType:
        """
        Takes a key or its path representation and returns a key.

        :param key:
                    A key or its path representation.
        :return:
                    A key.
        """
        store_key_type = self.store_key_type()

        if isinstance(key, store_key_type):
            return key

        if isinstance(key, str):
            key = FilePath(key)

        return store_key_type.from_path(key)

    def code_repr(self) -> CodeRepresentation:
        cls = type(self)

        import_dict: ImportDict = get_import_dict(code_repr(cls))

        cli_repr = self.cli_repr()

        # TODO: Check this is correct
        return import_dict, f"{cls.__name__}.from_cli_repr(\"{cli_repr}\")"