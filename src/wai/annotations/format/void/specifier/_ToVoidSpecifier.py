from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import Annotation, Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundUnion
from ....core.stage.specifier import SinkStageSpecifier


class ToVoidSpecifier(
    SinkStageSpecifier[DomainSpecifier[Instance[Data, Annotation]]]
):
    """
    Specifier for the to-void sink.
    """
    @classmethod
    def name(cls) -> str:
        return "To Void"

    @classmethod
    def description(cls) -> str:
        return "Consumes instances without writing them."

    @classmethod
    def bound(cls) -> InstanceTypeBoundUnion:
        return InstanceTypeBoundUnion.any()

    @classmethod
    def components(
            cls,
            domains: Tuple[Type[DomainSpecifier[Instance[Data, Annotation]]]]
    ) -> Tuple[Type[Component], ...]:
        from ..component import ToVoid
        return ToVoid,
