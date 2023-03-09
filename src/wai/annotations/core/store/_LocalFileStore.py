import os
from typing import Dict, Type, Union

from wai.common.cli.options import TypedOption

from ..util import recursive_iglob
from ..util.path import FilePath, FilePathLike, PathKey, path_to_str
from .key import StoreKey
from ._ReadableStore import ReadableStore
from ._WritableStore import WritableStore


class LocalFileStoreKey(StoreKey):
    """
    A store-key for the local filesystem.
    """
    def __init__(self, path: Union[FilePathLike, str]):
        self._path: FilePath = FilePath(path) if isinstance(path, str) else path.as_file_path()
        self._normalised = self._normalise2(self._path)

    def __hash__(self) -> int:
        return hash(self._normalised)

    @property
    def original_path(self) -> FilePath:
        return self._path

    @classmethod
    def from_path(cls: Type['LocalFileStoreKey'], path: FilePathLike) -> 'LocalFileStoreKey':
        return LocalFileStoreKey(path)

    def __eq__(self, other):
        return isinstance(other, LocalFileStoreKey) and other._normalised == self._normalised

    def as_path_key(self) -> PathKey:
        return self._normalised

    @staticmethod
    def _normalise2(path: FilePath) -> PathKey:
        """
        Creates a normalised form of any file-path as a path-key.
        """
        # Get the canonical path to the file, and split off the drive
        drive, filepath = os.path.splitdrive(os.path.realpath(path))

        # Convert absolute paths into paths relative to the root
        filepath = os.path.relpath(filepath, '/')

        # Prefix the drive as a path
        if drive.endswith(":"):
            # Path starts with a drive letter, format = [drive-letter]/[path-from-drive-root]
            filepath = os.path.join(drive[:-1], filepath)
        elif drive != "":
            # Path starts with a UNC sharepoint, format = [host]/[share]/[path-from-share-root]
            filepath = os.path.join(drive[2:], filepath)

        return PathKey(filepath)

    @staticmethod
    def _normalise(path: FilePath) -> PathKey:
        """
        Creates a normalised form of any file-path as a path-key.

        Left for posterity in-case _normalise2 is not suitable (may want to preserve link names in path).
        """
        drive, filepath = os.path.splitdrive(os.path.normcase(path))

        # Convert absolute paths into paths relative to the root, remembering
        # whether we started with an absolute or relative path
        path_is_absolute = False
        while os.path.isabs(filepath):
            path_is_absolute = True
            filepath = filepath[1:]

        # Prefix an identifier which makes the path relative, but reconstructible into the original path
        if drive.endswith(":"):
            # Path starts with a drive letter, format = drive/[drive-letter]/[path-from-drive-root]
            filepath = os.path.join("drive", drive[:-1], filepath)
        elif drive != "":
            # Path starts with a UNC sharepoint, format = sharepoint/[host]/[share]/[path-from-share-root]
            filepath = os.path.join("sharepoint", drive[2:], filepath)
        elif path_is_absolute:
            # Absolute path with no drive, format = absolute/[path-from-root]
            filepath = os.path.join("absolute", filepath)
        else:
            # Relative path, format = relative/[path-from-relative-location]
            filepath = os.path.join("relative", filepath)

        # Up-level (../) segments will be collapsed, so need to preserve these, but in a way that
        # distinguishes them from other uses of '..'. The only way is to replace all '..' occurrences
        # with some string that still contains '..'. We choose "..'" as it is less garish than other
        # options, but it still means that paths containing other uses of '..' will have them butchered,
        # which is hopefully a rare-enough occurrence to be acceptable. We don't care about same-level
        # (./) segments, or redundant slashes, as these don't change the meaning of the original path.
        filepath.replace("..", "..'")

        return PathKey(filepath)


class LocalFileStore(ReadableStore[LocalFileStoreKey], WritableStore[LocalFileStoreKey]):
    """
    Store representing the file system of the local machine.
    """
    root_dir: str = TypedOption(
        "-r", "--root",
        type=str,
        default=".",
        help="the root directory to which keys are relative",
        metavar="DIR"
    )

    def read_all(self, pattern: str, skip_data: bool = False) -> Dict[LocalFileStoreKey, bytes]:
        return {
            LocalFileStoreKey(os.path.relpath(path, self.root_dir)): self._read_file(path) if not skip_data else b''
            for path in recursive_iglob(os.path.join(self.root_dir, pattern))
        }

    def read(self, key: LocalFileStoreKey) -> bytes:
        return self._read_file(path_to_str(key.original_path))

    @staticmethod
    def _read_file(path: str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()

    def _write(self, key: LocalFileStoreKey, data: bytes):
        path = os.path.join(self.root_dir, key.original_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            file.write(data)

    def store_key_type(self) -> Type[LocalFileStoreKey]:
        return LocalFileStoreKey
