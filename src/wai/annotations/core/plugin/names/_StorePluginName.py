from typing import Optional

from .constants import PLUGIN_NAME_MATCHER
from ._PluginName import PluginName


class StorePluginName(PluginName):
    @classmethod
    def _validate_name(cls, name: str) -> Optional[str]:
        if PLUGIN_NAME_MATCHER(name) is None:
            return f"Store plugin name must be dash-separated lowercase letters but was '{name}'"
        return None
