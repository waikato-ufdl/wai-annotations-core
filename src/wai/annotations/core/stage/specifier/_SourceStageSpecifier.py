from abc import abstractmethod
from typing import Generic, Tuple, Type, TypeVar

from ...component import Component
from ...domain.specifier import DomainSpecifier
from ...plugin.specifier import PluginSpecifier
from ..bounds import InstanceTypeBoundUnion

SourceDomain = TypeVar('SourceDomain', bound=DomainSpecifier)


class SourceStageSpecifier(PluginSpecifier, Generic[SourceDomain]):
    """
    Class which specifies the components available to read a given format.
    """
    @classmethod
    @abstractmethod
    def bound(cls) -> InstanceTypeBoundUnion:
        """
        The bound on the types of instances this source can produce.
        """
        raise NotImplementedError(cls.bound.__qualname__)

    @classmethod
    @abstractmethod
    def components(cls, domain: Type[SourceDomain]) -> Tuple[Type[Component], ...]:
        """
        The components which make up the stage, in order of application.
        """
        raise NotImplementedError(cls.components.__qualname__)
