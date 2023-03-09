from abc import ABC, abstractmethod


class PluginSpecifier(ABC):
    """
    Base-class for specifier-types which introduce new functionality to
    wai.annotations.
    """
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
        Gets a short descriptive name for the plugin.
        """
        raise NotImplementedError(cls.name.__qualname__)

    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """
        Gets a longer description of the plugin.
        """
        raise NotImplementedError(cls.description.__qualname__)
