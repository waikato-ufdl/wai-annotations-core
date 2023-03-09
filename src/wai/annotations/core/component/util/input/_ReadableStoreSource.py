import os.path
from dataclasses import dataclass
from itertools import chain
from typing import ContextManager, List, TextIO, Tuple, Optional, Iterable, Iterator, Type

from wai.common import ClassRegistry
from wai.common.cli.options import TypedOption, Option, ClassOption
from wai.common.iterate import random

from ....plugin import get_all_plugins_by_type
from ....store import ReadableStore, LocalFileStore
from ....store.key import StoreKey
from ....store.specifier import StoreSpecifier
from ....stream import ThenFunction, DoneFunction
from ....stream.util import ProcessResource, ProcessState
from ....util import OptionalContextManager, chain_map, recursive_iglob, read_file_list, InstanceState, unique
from ..._SourceComponent import SourceComponent
from .._WithRandomness import WithOptionalRandomness

@dataclass
class ReadableStoreItem:
    key: StoreKey           # The key to the file in the readable store
    data: bytes             # The file data
    store: ReadableStore    # The store (for accessing related files)
    is_negative: bool       # Whether the file was specified as a negative example
    common_prefix: str      # The common path prefix for all files



STORE_CLASS_REGISTRY = ClassRegistry()
for name, cls in get_all_plugins_by_type().stores.items():
    if cls.is_readable():
        STORE_CLASS_REGISTRY.alias(cls, str(name))


def _init_store(self: 'ReadableStoreSource') -> ReadableStore:
    return self.store_type_specifier.store_type()(self.store_options)


class ReadableStoreSource(
    WithOptionalRandomness,
    SourceComponent[ReadableStoreItem]
):
    """
    Source which yields files from a readable store.
    """
    # The type of store to write to
    store_type_specifier: Type[StoreSpecifier[ReadableStore]] = ClassOption(
        "-s", "--store",
        registry=STORE_CLASS_REGISTRY,
        default=LocalFileStore,
        help="the store to read from",
        metavar="STORE"
    )

    # The options to the store
    store_options: List[str] = TypedOption(
        "-S", "--store-options",
        type=str,
        nargs="+",
        action="concat",
        help="the options to the store",
        metavar="STORE"
    )

    # The names of input files to read
    inputs: List[str] = TypedOption(
        "-i", "--input",
        type=str,
        metavar="PATH",
        action="concat"
    )

    # The names of files to load input lists from
    input_files: List[str] = TypedOption(
        "-I", "--inputs-file",
        type=str,
        metavar="FILENAME",
        action="concat"
    )

    # The names of files to include in the conversion without annotations
    negatives: List[str] = TypedOption(
        "-n", "--negative",
        type=str,
        metavar="PATH",
        action="concat"
    )

    # The names of files to load negative lists from
    negative_files: List[str] = TypedOption(
        "-N", "--negatives-file",
        type=str,
        metavar="FILENAME",
        action="concat"
    )

    # The filename to write read files to
    output_filename: Optional[str] = TypedOption(
        "-o", "--output-file",
        type=str,
        metavar="FILENAME",
        help="optional file to write read filenames into"
    )

    # The open file handle to write to
    output_file_handle: ContextManager[Optional[TextIO]] = ProcessResource(
        lambda self: OptionalContextManager(
            open(self.output_filename, "w") if self.output_filename is not None
            else None
        )
    )

    # The store to read from
    store: ReadableStore = ProcessState(_init_store)

    def produce(
            self,
            then: ThenFunction[ReadableStoreItem],
            done: DoneFunction
    ):
        # Warn the user if no input files were specified
        if len(self.input_file_keys) + len(self.negative_file_keys) == 0:
            self.logger.warning("No input files selected to convert")

        # Work out the common prefix for all files
        prefix: str = os.path.commonpath([*self.input_file_keys, *self.negative_file_keys])

        self.process_keys(self.input_file_keys, False, prefix, then)
        self.process_keys(self.negative_file_keys, True, prefix, then)

        with self.output_file_handle as output_file_handle:
            if output_file_handle is not None:
                output_file_handle.close()

        done()

    def process_keys(
            self,
            keys: Tuple[StoreKey, ...],
            is_negatives: bool,
            common_prefix: str,
            then: ThenFunction[ReadableStoreItem]
    ):
        if self.has_random:
            keys = tuple(random(iter(keys), self.random))

        for key in keys:
            _, data = self.store.read_exact(key)
            then(ReadableStoreItem(key, data, self.store, is_negatives, common_prefix))
            with self.output_file_handle as output_file_handle:
                if output_file_handle is not None:
                    output_file_handle.write(f"{key.path},{'true' if is_negatives else 'false'}\n")

    @InstanceState
    def input_file_keys(self) -> Tuple[StoreKey, ...]:
        return tuple(unique(self.load_keys(self.inputs, self.input_files)))

    @InstanceState
    def negative_file_keys(self) -> Tuple[StoreKey, ...]:
        return tuple(unique(self.load_keys(self.negatives, self.negative_files)))

    def load_keys(self, direct_files: Iterable[str], list_files: Iterable[str]) -> Iterator[StoreKey]:
        yield from (
            key
            for path in self.load_paths(direct_files, list_files)
            for key in self.store.read_all(path, skip_data=True).keys()
        )

    @classmethod
    def load_paths(cls, direct_files: Iterable[str], list_files: Iterable[str]) -> Iterator[str]:
        return chain(
            direct_files,
            chain_map(read_file_list, chain_map(recursive_iglob, list_files))
        )

    @classmethod
    def get_help_text_for_inputs_option(cls) -> str:
        return "Input files (can use glob syntax)"

    @classmethod
    def get_help_text_for_input_files_option(cls) -> str:
        return "Files containing lists of input files (can use glob syntax)"

    @classmethod
    def get_help_text_for_negatives_option(cls) -> str:
        return "Files that have no annotations (can use glob syntax)"

    @classmethod
    def get_help_text_for_negative_files_option(cls) -> str:
        return "Files containing lists of negative files (can use glob syntax)"

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.inputs:
            return cls.get_help_text_for_inputs_option()
        if option is cls.input_files:
            return cls.get_help_text_for_input_files_option()
        if option is cls.negatives:
            return cls.get_help_text_for_negatives_option()
        if option is cls.negative_files:
            return cls.get_help_text_for_negative_files_option()
        return super().get_help_text_for_option(option)

