from typing import Any, Generic, Optional, Tuple, Type, TypeVar, Union, TYPE_CHECKING

from wai.annotations.core.domain import Annotation, Data, Instance
if TYPE_CHECKING:
    from ._InstanceTypeBoundUnion import InstanceTypeBoundUnion


RawInstanceTypeBound = Union[   # A single bound for an instance-type is either...
    Type[Instance],             # a specific instance-type to bound to, or...
    Tuple[                      # a pair of...
        Type[Data],             # the data-type that the instance-type must have, and...
        Type[Annotation]        # the annotation-type the instance-type must have.
    ]
]


class InstanceTypeBound:
    """
    Represents a single bound against which instance-types can be
    compared for compatibility. Similar to the bound on a generic type.
    """
    def __init__(
            self,
            bound: RawInstanceTypeBound
    ):
        InstanceTypeBound._check_is_single_bound(bound)
        self._bound = bound

    @property
    def data_type(self) -> Type[Data]:
        return (
            self._bound[0] if isinstance(self._bound, tuple)
            else self._bound.data_type()
        )

    @property
    def annotation_type(self) -> Type[Annotation]:
        return (
            self._bound[1] if isinstance(self._bound, tuple)
            else self._bound.annotation_type()
        )

    @property
    def as_pair(self) -> Tuple[Type[Data], Type[Annotation]]:
        return (
            self._bound if isinstance(self._bound, tuple)
            else (self._bound.data_type(), self._bound.annotation_type())
        )

    @property
    def instance_type(self) -> Optional[Type[Instance]]:
        return (
            None if isinstance(self._bound, tuple)
            else self._bound
        )

    def __str__(self):
        if isinstance(self._bound, tuple):
            return f"{Instance.__name__}[{self._bound[0].__name__}, {self._bound[1].__name__}]"
        else:
            return f"{self._bound.__name__}"

    @classmethod
    def _check_is_single_bound(
            cls,
            value: Any
    ):
        """
        Checks if the argument is actually an InstanceTypeBound.

        :param value:
                    The value to check.
        """
        if isinstance(value, type):
            if not issubclass(value, Instance):
                raise ValueError(f"Must be a type of {Instance.__qualname__}, got {value.__qualname__}")
        elif isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError(f"Must be tuple of length 2, got {len(value)}")
            elif not isinstance(value[0], type):
                raise ValueError(f"First tuple element must be a type, got {type(value[0]).__qualname__}")
            elif not issubclass(value[0], Data):
                raise ValueError(f"First tuple element must be a type of {Data.__qualname__}, got {value[0].__qualname__}")
            elif not isinstance(value[1], type):
                raise ValueError(f"Second tuple element must be a type, got {type(value[1]).__qualname__}")
            elif not issubclass(value[1], Annotation):
                raise ValueError(f"Second tuple element must be a type of {Annotation.__qualname__}, got {value[1].__qualname__}")
        else:
            raise TypeError(f"Must be a type or a tuple, got {type(value)}")

    def is_sub_type(
            self,
            other: 'InstanceTypeBound'
    ) -> bool:
        """
        Checks if this single instance-type-bound is a sub-type of
        another single instance-type-bound.
        """
        if isinstance(self._bound, tuple):
            if isinstance(other._bound, tuple):
                return issubclass(self._bound[0], other._bound[0]) and issubclass(self._bound[1], other._bound[1])
            else:
                return False
        else:
            if isinstance(other._bound, tuple):
                return issubclass(self._bound.data_type(), other._bound[0]) and issubclass(self._bound.annotation_type(), other._bound[1])
            else:
                return issubclass(self._bound, other._bound)

    def intersection_bound(
            self,
            other: 'InstanceTypeBound'
    ) -> Optional['InstanceTypeBound']:
        """
        Gets a single instance-type-bound that is the intersection of
        this and another bound.

        :return:
                    The intersection bound, or None if no bound exists.
        """
        if isinstance(self._bound, tuple):
            if isinstance(other._bound, tuple):
                data_type = (
                    self._bound[0] if issubclass(self._bound[0], other._bound[0])
                    else other._bound[0] if issubclass(other._bound[0], self._bound[0])
                    else None
                )
                annotation_type = (
                    self._bound[1] if issubclass(self._bound[1], other._bound[1])
                    else other._bound[1] if issubclass(other._bound[1], self._bound[1])
                    else None
                )
                return (
                    InstanceTypeBound((data_type, annotation_type))
                    if data_type is not None and annotation_type is not None
                    else None
                )
            else:
                return (
                    other if other.is_sub_type(self)
                    else None
                )
        else:
            if isinstance(other._bound, tuple):
                return (
                    self if self.is_sub_type(other)
                    else None
                )
            else:
                return (
                    self if self.is_sub_type(other)
                    else other if other.is_sub_type(self)
                    else None
                )

    def to_union(self) -> 'InstanceTypeBoundUnion':
        from ._InstanceTypeBoundUnion import InstanceTypeBoundUnion
        return InstanceTypeBoundUnion(self)

    @classmethod
    def any(cls) -> 'InstanceTypeBound':
        return InstanceTypeBound((Data, Annotation))
