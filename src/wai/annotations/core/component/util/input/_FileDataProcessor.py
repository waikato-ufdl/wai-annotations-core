from abc import abstractmethod
from typing import Generic

from ....store import ReadableStore
from ....store.key import StoreKey
from ....stream import ThenFunction, DoneFunction
from ....stream.util import RequiresNoFinalisation
from ..._ProcessorComponent import ProcessorComponent, OutputElementType
from ._ReadableStoreSource import ReadableStoreItem


class FileDataProcessor(
    RequiresNoFinalisation,
    ProcessorComponent[
        ReadableStoreItem,
        OutputElementType
    ],
    Generic[OutputElementType]
):
    """
    Processor which converts data read from annotation/negative files specified
    by a ReadableStoreSource into more useful types.
    """
    def process_element(
            self,
            element: ReadableStoreItem,
            then: ThenFunction[OutputElementType],
            done: DoneFunction
    ):
        key, data, store, prefix, is_negative = (
            element.key, element.data, element.store, element.common_prefix, element.is_negative
        )

        if is_negative:
            self.parse_negative_file(key, data, store, prefix, then)
        else:
            self.parse_annotation_file(key, data, store, prefix, then)

    @abstractmethod
    def parse_annotation_file(
            self,
            key: StoreKey,
            data: bytes,
            store: ReadableStore,
            common_prefix: str,
            then: ThenFunction[OutputElementType]
    ):
        """
        Parses a positive annotation file into the output type.

        :param key:
                    The store-key from which the annotation-file was read.
        :param data:
                    The contents of the annotation file.
        :param store:
                    The store from which the file was read.
        :param then:
                    The forwarding function for outputting the parsed value.
        """
        raise NotImplementedError(self.parse_annotation_file.__qualname__)

    @abstractmethod
    def parse_negative_file(
            self,
            key: StoreKey,
            data: bytes,
            store: ReadableStore,
            common_prefix: str,
            then: ThenFunction[OutputElementType]
    ):
        """
        Parses a negatively-annotated file into the output type.

        :param key:
                    The store-key from which the file was read.
        :param data:
                    The contents of the file.
        :param store:
                    The store from which the file was read.
        :param then:
                    The forwarding function for outputting the parsed value.
        """
        raise NotImplementedError(self.parse_negative_file.__qualname__)
