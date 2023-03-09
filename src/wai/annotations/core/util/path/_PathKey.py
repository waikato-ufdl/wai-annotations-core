import os.path

from ._FilePath import FilePath
from ._PathKeyLike import PathKeyLike


class PathKey(PathKeyLike, FilePath):
    """
    A normalised representation of file-paths.

    Ensures that the path:
     - is relative (to some root)
     - includes a filename (i.e. is not just a directory)
     - does not start with '../' or './' (i.e. is either just a filename or starts with a top-level directory name)
     - is normalised (see os.path.normpath)
    """
    def __init__(self, path: str):
        """
        Validate a str as a PathKey.

        :param path:
                    The path to parse.
        :raise ValueError:
                    - The path is not relative.
                    - The path does not include a filename component.
                    - The normalised path is relative above its implied root (starts with ../).
        """
        # Normalise
        normpath = os.path.normpath(path)

        # Must be relative to some root
        if os.path.isabs(path):
            raise ValueError(
                f"PathKeys cannot be absolute (path should be relative to some root)\n"
                f"Received {path}"
            )

        # Cannot be relative outside the root
        if normpath.startswith(f"..{os.sep}") or normpath == "..":
            raise ValueError(
                f"Path-keys cannot be relative above the root\n"
                f"Received {path}"
            )

        super().__init__(normpath)

    def as_path_key(self) -> 'PathKey':
        return self
