from abc import ABC, abstractmethod
from typing import Any, Optional

from wai.annotations.core.plugin.error import BadPluginName


class PluginName(ABC):
    @classmethod
    @abstractmethod
    def _validate_name(cls, name: str) -> Optional[str]:
        raise NotImplementedError(cls._validate_name.__qualname__)

    def __init__(self, name: str):
        reason = self._validate_name(name)
        if reason is not None:
            raise BadPluginName(name, reason)
        self._name = name

    def __str__(self) -> str:
        return self._name

    def __eq__(self, other: Any) -> bool:
        return str(other) == self._name

    def __hash__(self) -> int:
        return hash(self._name)
