import inspect
from abc import ABC, abstractmethod
from typing import Tuple, TypeVar, Generic, Optional, Type, TYPE_CHECKING

from ..util.path import PathKey, PathKeyLike
from ._Annotation import Annotation
from ._Data import Data

if TYPE_CHECKING:
    from .specifier import DomainSpecifier

DataType = TypeVar("DataType", bound=Data)
AnnotationType = TypeVar("AnnotationType", bound=Annotation)
SelfType = TypeVar("SelfType", bound='Instance')


class Instance(
    Generic[DataType, AnnotationType],
    ABC
):
    """
    A single item in a data-set.
    """
    def __init__(
            self,
            key: PathKeyLike,
            data: Optional[DataType],
            annotation: Optional[AnnotationType]
    ):
        self._key: PathKey = key.as_path_key()
        self._data: Optional[DataType] = data
        self._annotation: Optional[AnnotationType] = annotation

    @property
    def key(self) -> PathKey:
        return self._key

    @property
    def data(self) -> Optional[DataType]:
        return self._data

    @classmethod
    @abstractmethod
    def data_type(cls) -> Type[DataType]:
        raise NotImplementedError(cls.data_type.__qualname__)

    @property
    def annotation(self) -> Optional[AnnotationType]:
        return self._annotation

    @classmethod
    @abstractmethod
    def annotation_type(cls) -> Type[AnnotationType]:
        raise NotImplementedError(cls.annotation_type.__qualname__)

    @classmethod
    @abstractmethod
    def domain_specifier(cls: Type[SelfType]) -> Type['DomainSpecifier[SelfType]']:
        raise NotImplementedError(cls.domain_specifier.__qualname__)

    @property
    def has_data(self) -> bool:
        """
        Whether this instance has data.
        """
        return self._data is not None

    @property
    def is_unannotated(self) -> bool:
        """
        Whether this instance is a negative instance (contains no annotations).
        """
        return self.annotation is None

    @classmethod
    def from_parts(
            cls: Type[SelfType],
            key: PathKeyLike,
            data: Optional[DataType],
            annotation: Optional[AnnotationType]
    ) -> SelfType:
        """
        Creates an instance from the key/data/annotation. All instance types must be
        capable of doing this.

        :param key:
                    The instance key.
        :param data:
                    The instance data.
        :param annotation:
                    The instance annotation.
        :return:
                    The instance.
        """
        # If the init method signature hasn't been changed, calling it should work
        if inspect.signature(Instance.__init__) == inspect.signature(cls.__init__):
            return cls(key, data, annotation)

        # Otherwise it must be reimplemented
        raise NotImplementedError(cls.from_parts.__qualname__)

    def parts(self) -> Tuple[PathKey, Optional[DataType], Optional[AnnotationType]]:
        """
        Spreads the instance into its component parts.
        """
        return self._key, self._data, self._annotation

    def __iter__(self):
        yield self._key
        yield self._data
        yield self._annotation
