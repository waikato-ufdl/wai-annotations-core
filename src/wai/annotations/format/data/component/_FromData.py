import os.path
from abc import abstractmethod
from typing import Type, TypeVar

from ....core.component.util.input import FileDataProcessor, ReadableStoreItem
from ....core.domain import Annotation, Data, Instance
from ....core.store import ReadableStore
from ....core.store.key import StoreKey
from ....core.stream import ThenFunction
from ....core.util.path import PathKey

InstanceType = TypeVar('InstanceType', bound=Instance[Data, Annotation])


class FromData(
    FileDataProcessor[
        ReadableStoreItem,  # FIXME: Bug: Python doesn't recognise that this generic parameter
                            #             is already specified in FileDataProcessor.
        InstanceType
    ]
):
    """
    Reader that reads in data files.
    """
    @classmethod
    @abstractmethod
    def instance_type(cls) -> Type[InstanceType]:
        raise NotImplementedError(cls.instance_type.__qualname__)

    def parse_annotation_file(
            self,
            key: StoreKey,
            data: bytes,
            store: ReadableStore,
            common_prefix: str,
            then: ThenFunction[InstanceType]
    ):
        then(
            self.instance_type().from_parts(
                PathKey(os.path.relpath(key.as_path_key(), common_prefix)),
                self.instance_type().data_type().from_data(data),
                None
            )
        )

    def parse_negative_file(
            self,
            key: StoreKey,
            data: bytes,
            store: ReadableStore,
            common_prefix: str,
            then: ThenFunction[InstanceType]
    ):
        # Negative files and annotation files are equivalent
        self.parse_annotation_file(key, data, store, then)
