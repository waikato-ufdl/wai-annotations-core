import base64
import re
from typing import Dict, List, Type

from wai.common.cli import CLIRepresentable
from wai.common.cli.options import TypedOption

from ..util import InstanceState
from .key import BasicStoreKey
from ._ReadableStore import ReadableStore
from ._WritableStore import WritableStore


class DictStoreMapping(CLIRepresentable):
    """
    A mapping from a key to a value in a DictStore. Is represented on the command-line
    as "[key]>[value]", where [key] is a path and [value] is Base64-encoded data.
    """
    # Not a valid character in a Base64 encoding, so can be used to find the start of the data
    KEY_VALUE_SEPARATOR: str = ">"

    def __init__(self, key: str, value: bytes):
        self._key = BasicStoreKey(key)
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    def cli_repr(self) -> str:
        return f"{self._key.path}{DictStoreMapping.KEY_VALUE_SEPARATOR}{base64.encodebytes(self._value).decode()}"

    @classmethod
    def from_cli_repr(cls: Type['DictStoreMapping'], cli_string: str) -> 'DictStoreMapping':
        # Find the last instance of the separator (which should precede the data segment)
        separator_index = cli_string.rfind(DictStoreMapping.KEY_VALUE_SEPARATOR)

        # Make sure a separator was supplied
        if separator_index == -1:
            raise ValueError(
                f"Couldn't parse CLI string '{cli_string}' into mapping, "
                f"separator '{DictStoreMapping.KEY_VALUE_SEPARATOR}' not found"
            )

        # The filename is everything up to the separator
        key = cli_string[:separator_index]

        # The value is Base64 encoded data after the separator
        value = base64.decodebytes(cli_string[separator_index + 1:].encode())

        return DictStoreMapping(key, value)


def _values_dict_init(self: 'DictStore') -> Dict[BasicStoreKey, bytes]:
    """
    Initialises the values_dict of a DictStore.
    """
    return {
        mapping.key: mapping.value
        for mapping in self.values
    }


class DictStore(ReadableStore[BasicStoreKey], WritableStore[BasicStoreKey]):
    """
    In-memory store which uses a dict internally.
    """
    # Command-line option to set the initial values in the store
    values: List[DictStoreMapping] = TypedOption(
        "-m", "--mapping",
        type=DictStoreMapping,
        nargs="+",
        action="concat",
        help="initial values in the store",
        metavar=f"KEY{DictStoreMapping.KEY_VALUE_SEPARATOR}BASE64"
    )

    # The runtime key-value store
    values_dict: Dict[BasicStoreKey, bytes] = InstanceState(_values_dict_init)

    def read(self, key: BasicStoreKey) -> bytes:
        if key not in self.values_dict:
            raise FileNotFoundError(key.path)
        return self.values_dict[key]

    def read_all(
            self,
            pattern: str,
            skip_data: bool = False
    ) -> Dict[BasicStoreKey, bytes]:
        # Compile the pattern
        fullmatch = re.compile(pattern).fullmatch

        # Return any matching keys
        return {
            self_key: value
            for self_key, value in self.values_dict.items()
            if fullmatch(self_key.path) is not None
        }

    def _write(self, key: BasicStoreKey, data: bytes):
        # Add the data to our dict
        self.values_dict[key] = data

    def store_key_type(self) -> Type[BasicStoreKey]:
        return BasicStoreKey

    def __contains__(self, item):
        return item in self.values_dict