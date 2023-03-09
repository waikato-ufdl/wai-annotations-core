import os.path

from ._FilePathLike import FilePathLike


class FilePath(FilePathLike):
    """
    A path that contains a filename component i.e. is not just a directory.
    """
    def __init__(self, path: str):
        """
        :param path:
                    The path to validate as containing a filename component.
        :raise ValueError:
                    If path doesn't contain a filename component.
        """
        # Must contain a filename part
        if os.path.basename(path) == "":
            raise ValueError(
                f"FilePaths may not be directories, received {path}"
            )

        self._path = path

    def as_file_path(self) -> 'FilePath':
        return self

    def __eq__(self, other):
        return isinstance(other, FilePath) and other._path == self._path

    def __hash__(self) -> int:
        return hash(self._path)

    def __fspath__(self) -> str:
        # Override default implementation as it causes a stack-overflow
        return self._path

    def __str__(self) -> str:
        return f"{type(self).__name__} '{self._path}'"