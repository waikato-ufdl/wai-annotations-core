from typing import Type

from pkg_resources import EntryPoint

from ..util import is_subtype, describe_value
from .error import BadPluginSpecifier
from .specifier import PluginSpecifier


def load_plugin_specifier_from_entry_point(
        name: str,
        entry_point: EntryPoint
) -> Type[PluginSpecifier]:
    """
    Loads a plugin specifier from an entry-point.

    :param name:
                The name of the plugin.
    :param entry_point:
                The entry-point to load from.
    :return:
                The plugin specifier.
    """
    # Try to load the (supposed) plugin specifier from the entry-point
    try:
        specifier = entry_point.load()

    # Type any errors raised during loading
    except Exception as e:
        raise BadPluginSpecifier(f"Error loading plugin '{name}': {e}") from e

    # Check it actually is a plugin specifier
    if not is_subtype(specifier, PluginSpecifier):
        raise BadPluginSpecifier(
            f"Plugin specifier '{name}' should be a sub-class of {PluginSpecifier.__qualname__}, "
            f"received {describe_value(specifier)}"
        )

    return specifier
