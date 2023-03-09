from os import PathLike, fsdecode, fspath
from typing import Union


def path_to_str(
        path: Union[
            str,
            bytes,
            PathLike
        ]
) -> str:
    """
    Normalises any path-like representation as a string.
    """
    return fsdecode(fspath(path))
