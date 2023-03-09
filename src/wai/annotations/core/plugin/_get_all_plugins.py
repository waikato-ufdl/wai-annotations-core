from typing import Dict, Type

from .specifier import PluginSpecifier
from ._get_all_plugin_names import get_all_plugin_names
from ._get_plugin_specifier_by_name import get_plugin_specifier_by_name


def get_all_plugins() -> Dict[str, Type[PluginSpecifier]]:
    """
    Gets all plugin specifiers registered with the system.
    """
    return {
        name: get_plugin_specifier_by_name(name)
        for name in get_all_plugin_names()
    }
