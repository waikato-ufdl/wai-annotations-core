from abc import abstractmethod
from typing import Tuple, Type, TypeVar

from ...component import Component
from ...domain.specifier import DomainSpecifier
from ...plugin.specifier import PluginSpecifier
from ..bounds import InstanceTypeBoundRelationship

InputDomain = TypeVar('InputDomain', bound=DomainSpecifier)
OutputDomain = TypeVar('OutputDomain', bound=DomainSpecifier)


class ProcessorStageSpecifier(PluginSpecifier):
    """
    Specifier for a conversion from one domain to another.
    """
    @classmethod
    @abstractmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        """
        Defines the relationship between the input instance-type and the output
        instance-type of this processor stage.
        """
        raise NotImplementedError(cls.bound_relationship.__qualname__)

    @classmethod
    @abstractmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[Component], ...]:
        """
        The components which make up the stage, in order of application.
        """
        raise NotImplementedError(cls.components.__qualname__)
