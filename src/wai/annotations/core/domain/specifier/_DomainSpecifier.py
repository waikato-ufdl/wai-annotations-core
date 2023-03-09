from abc import abstractmethod
from typing import Type, TypeVar, Generic

from ...plugin.specifier import PluginSpecifier
from .._Annotation import Annotation
from .._Data import Data
from .._Instance import Instance

InstanceType = TypeVar('InstanceType', bound=Instance)
DataType = TypeVar('DataType', bound=Data)
AnnotationType = TypeVar('AnnotationType', bound=Annotation)
ExpectedType = TypeVar('ExpectedType')


class DomainSpecifier(PluginSpecifier, Generic[InstanceType]):
    """
    Class which specifies the internal representation of data/annotations in
    a specific domain (e.g. images, videos, etc.).
    """
    @classmethod
    def data_type(cls: 'Type[DomainSpecifier[Instance[DataType, Annotation]]]') -> Type[DataType]:
        return cls.instance_type().data_type()

    @classmethod
    def annotations_type(cls: 'Type[DomainSpecifier[Instance[Data, AnnotationType]]]') -> Type[AnnotationType]:
        return cls.instance_type().annotation_type()

    @classmethod
    @abstractmethod
    def instance_type(cls) -> Type[InstanceType]:
        """
        The type of instance in this domain.
        """
        raise NotImplementedError(cls.instance_type.__qualname__)
