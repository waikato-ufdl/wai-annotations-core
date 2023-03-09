from typing import Dict, Type

from .specifier import PluginSpecifier


# A cache of loaded specifiers for plugins
__cache: Dict[str, Type[PluginSpecifier]] = {}


def is_cached(name: str) -> bool:
    """
    Whether a plugin exists in the cache by a given name.

    :param name:    The plugin name.
    :return:        Whether the cache
    """
    return name in __cache


def get_cached(name: str) -> Type[PluginSpecifier]:
    """
    Gets a cached plugin specifier.

    :param name:    The name of the plugin to get.
    :return:        The plugin specifier.
    """
    return __cache[name]


def set_cache(name: str, specifier: Type[PluginSpecifier]):
    """
    Adds a specifier to the cache.

    :param name:        The name to give the specifier.
    :param specifier:   The specifier.
    """
    __cache[name] = specifier
