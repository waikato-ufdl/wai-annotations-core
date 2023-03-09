from typing import Optional

from .domain_suffix.constants import DOMAIN_CODE_MATCHER
from .domain_suffix import DomainCode
from ._PluginName import PluginName


class DomainPluginName(PluginName):
    @classmethod
    def _validate_name(cls, name: str) -> Optional[str]:
        if DOMAIN_CODE_MATCHER(name) is None:
            return f"Domain plugin name must be 2-letter domain code but was '{name}'"
        return None

    @property
    def domain_code(self) -> DomainCode:
        return DomainCode(str(self))
