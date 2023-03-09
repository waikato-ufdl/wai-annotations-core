from typing import List, Optional, Tuple, Type, Union, TYPE_CHECKING

from ...domain import Annotation, Data, Instance
from ..util import reduce_subsumes
from ._InstanceTypeBound import InstanceTypeBound, RawInstanceTypeBound

if TYPE_CHECKING:
    from ...domain.specifier import DomainSpecifier


class InstanceTypeBoundUnion:
    """
    Class which represents bounds against which instance-types can be
    compared for compatibility. Similar to the bound on a generic type.
    """
    def __init__(
            self,
            bound: Union[InstanceTypeBound, RawInstanceTypeBound],
            *bounds: Union[InstanceTypeBound, RawInstanceTypeBound]
    ):
        self._bounds = reduce_subsumes(
            InstanceTypeBound.is_sub_type,
            *(
                b if isinstance(b, InstanceTypeBound) else InstanceTypeBound(b)
                for b in (bound, *bounds)
            )
        )

    def __str__(self):
        return " | ".join(map(str, self._bounds))

    def __iter__(self):
        return iter(self._bounds)

    @property
    def data_types(self) -> List[Type[Data]]:
        return reduce_subsumes(
            lambda a, b: issubclass(a, b),
            *(bound.data_type for bound in self._bounds)
        )

    @property
    def annotation_types(self) -> List[Type[Annotation]]:
        return reduce_subsumes(
            lambda a, b: issubclass(a, b),
            *(bound.annotation_type for bound in self._bounds)
        )

    @property
    def as_pairs(self) -> List[Tuple[Type[Data], Type[Annotation]]]:
        return [
            bound.as_pair
            for bound in self._bounds
        ]

    @property
    def instance_types(self) -> List[Type[Instance]]:
        return [
            bound.instance_type
            for bound in self._bounds
            if bound.instance_type is not None
        ]

    @property
    def as_single(self) -> Optional[Type[Instance]]:
        instance_types = self.instance_types
        return (
            instance_types[0] if len(instance_types) == 1
            else None
        )

    def intersection_bound(
            self,
            other: 'InstanceTypeBoundUnion'
    ) -> Optional['InstanceTypeBoundUnion']:
        candidate_bounds: List[InstanceTypeBound] = []

        for self_bound in self._bounds:
            for other_bound in other._bounds:
                candidate_bound = self_bound.intersection_bound(other_bound)
                if candidate_bound is not None:
                    candidate_bounds.append(candidate_bound)

        if len(candidate_bounds) == 0:
            return None

        return InstanceTypeBoundUnion(*candidate_bounds)

    @staticmethod
    def for_domain(domain: Type['DomainSpecifier']) -> 'InstanceTypeBoundUnion':
        return InstanceTypeBoundUnion(domain.instance_type())

    @staticmethod
    def any() -> 'InstanceTypeBoundUnion':
        return InstanceTypeBoundUnion(InstanceTypeBound.any())
