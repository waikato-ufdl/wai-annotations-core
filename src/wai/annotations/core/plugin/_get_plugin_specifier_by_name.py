from typing import Tuple, Type

from pkg_resources import EntryPoint

from .error import *
from .specifier import PluginSpecifier
from ._cache import is_cached, get_cached, set_cache
from ._load_plugin_specifier_from_entry_point import load_plugin_specifier_from_entry_point
from ._plugin_entry_points import plugin_entry_points


def get_plugin_specifier_by_name(
        name: str
) -> Type[PluginSpecifier]:
    """
    Gets a plugin specifier from the plugin with the given name.

    :param name:
                The name of the plugin.
    :return:
                The specifier.
    """
    # Check the cache
    if is_cached(name):
        return get_cached(name)

    # Get the plugin entry-points for the given name
    entry_points: Tuple[EntryPoint, ...] = tuple(plugin_entry_points(name))

    # Make sure there is one and only one entry-point for the name
    if len(entry_points) > 1:
        # If this name is multiply-defined, perhaps others are too?
        MultiplyDefinedPlugins.check_entry_points(*plugin_entry_points())
    elif len(entry_points) == 0:
        raise UnknownPluginName(name)

    # Get the plugin entry-point
    plugin_entry_point: EntryPoint = entry_points[0]

    # Load the plugin specifier
    plugin_specifier = load_plugin_specifier_from_entry_point(name, plugin_entry_point)

    # Cache it
    set_cache(name, plugin_specifier)

    return plugin_specifier
