from argparse import Namespace
import os
from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory
from typing import List, Optional, Type, TypeVar, Iterator, IO, Tuple, Iterable, Union

from wai.common import ClassRegistry
from wai.common.cli.options import TypedOption, Option, ClassOption

from ....plugin import get_all_plugins_by_type
from ....store import LocalFileStore, WritableStore
from ....store.specifier import StoreSpecifier
from ....stream import Pipeline
from ....stream.util import ProcessState
from ....util.path import FilePathLike
from ..._SinkComponent import SinkComponent

ElementType = TypeVar("ElementType")

STORE_CLASS_REGISTRY = ClassRegistry()
for name, cls in get_all_plugins_by_type().stores.items():
    if cls.is_writable():
        STORE_CLASS_REGISTRY.alias(cls, str(name))

def _init_store(self: 'WritableStoreSink') -> WritableStore:
    return self.store_type_specifier.store_type()(self.store_options)


class WritableStoreSink(
    SinkComponent[ElementType],
    ABC
):
    """
    Base class for writers which can write a specific external format to a writable store.
    """
    # The type of store to write to
    store_type_specifier: Type[StoreSpecifier[WritableStore]] = ClassOption(
        "-s", "--store",
        registry=STORE_CLASS_REGISTRY,
        default=LocalFileStore,
        help="the store to write to",
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

    # The file or directory to write into
    output = TypedOption(
        "-o", "--output",
        type=str,
        metavar="PATH",
        required=True
    )

    store: WritableStore = ProcessState(_init_store)

    def write(self, contents: bytes, path: Union[None, FilePathLike, str] = None):
        """
        Writes the given file data to the output store.

        :param contents:
                    The data to write.
        :param path:
                    The path in the store to write to. Ignored if the
                    sink expects a filename.
        """
        if self.expects_directory and path is None:
            raise Exception("Must provide a path")



        self.store.write(
            self.output if self.expects_file else os.path.join(self.output, path),
            contents
        )

    @property
    def output_path(self) -> str:
        """
        The directory this writer is writing to.
        """
        # Get the path from the 'output' option
        output_path = self.output
        if self.expects_file:
            output_path = os.path.dirname(output_path)

        # Make sure the path ends with a slash
        if not output_path.endswith(os.path.sep):
            output_path += os.path.sep

        return output_path

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.output:
            return cls.get_help_text_for_output_option()
        return super().get_help_text_for_option(option)

    @classmethod
    @abstractmethod
    def get_help_text_for_output_option(cls) -> str:
        """
        Gets the help text describing what type of path the 'output' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        raise NotImplementedError(cls.get_help_text_for_option.__qualname__)

    @property
    @abstractmethod
    def expects_file(self) -> bool:
        """
        Whether this writer expects the 'output' option to specify
        a file, or if not, a directory.
        """
        raise NotImplementedError(type(self).expects_file.__qualname__)

    @property
    def expects_directory(self) -> bool:
        """
        Whether this writer expects the 'output' option to specify
        a directory, or if not, a file.
        """
        return not self.expects_file


class ExpectsFile:
    """
    Mixin class which declares the local file-writer expects a file-name
    for its 'output' option.
    """
    @property
    def expects_file(self) -> bool:
        return True

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the file to write to"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls, WritableStoreSink):
            raise Exception(
                f"{ExpectsFile.__qualname__} can only be used in conjunction "
                f"with the {WritableStoreSink.__qualname__} class"
            )


class ExpectsDirectory:
    """
    Mixin class which declares the local file-writer expects a directory-name
    for its 'output' option.
    """
    @property
    def expects_file(self) -> bool:
        return False

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the directory to write to"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls, WritableStoreSink):
            raise Exception(
                f"{ExpectsDirectory.__qualname__} can only be used in conjunction "
                f"with the {WritableStoreSink.__qualname__} class"
            )


def iterate_files(pipeline: Pipeline, source: Optional[Iterable] = None) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Iterates through the files written by a pipeline.

    :param pipeline:    The pipeline (must end in a local file-writer).
    :param source:      The source to provide stream elements to the pipeline.
                        Uses the fixed source if none given.
    :return:            An iterator of file-name, file pairs.
    """
    # Get the writer from the end of the pipeline
    writer = pipeline.sink

    # Make sure the pipeline ends with a local file-writer
    if not isinstance(writer, WritableStoreSink):
        raise Exception(
            "Can only iterate files for pipelines that end in "
            "a local file-writer"
        )

    # Create a temporary directory to write into
    with TemporaryDirectory() as temp_directory:
        # Format a new output location within the temp directory
        new_output = (
            temp_directory
            if not writer.expects_file
            else os.path.join(temp_directory, os.path.basename(writer.output))
        )

        # Create a clone of the writer with the new output
        temp_writer = type(writer)(Namespace(**vars(writer.namespace)))
        temp_writer.store = LocalFileStore()
        temp_writer.output = new_output

        # Create a new pipeline with the new output
        new_pipeline = Pipeline(
            pipeline.source if pipeline.has_source else None,
            pipeline.processors,
            temp_writer
        )

        # Execute the new pipeline
        new_pipeline.process(source)

        # Iterate through all written files
        for dirpath, dirnames, filenames in os.walk(temp_directory):
            for filename in filenames:
                # Create a filename relative to the temp directory
                full_filename = os.path.normpath(
                    os.path.join(os.path.relpath(dirpath, temp_directory), filename)
                )

                # Open the temp file and yield its contents
                with open(os.path.join(temp_directory, full_filename), "rb") as file:
                    yield full_filename, file
