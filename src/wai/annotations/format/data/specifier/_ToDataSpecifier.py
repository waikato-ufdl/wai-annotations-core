from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import Annotation, Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundUnion
from ....core.stage.specifier import SinkStageSpecifier


class ToDataSpecifier(
    SinkStageSpecifier[DomainSpecifier[Instance[Data, Annotation]]]
):
    """
    Specifier for the to-data sink.
    """
    @classmethod
    def name(cls) -> str:
        return "To Data"

    @classmethod
    def description(cls) -> str:
        return "Produces unannotated instances from data-files."

    @classmethod
    def bound(cls) -> InstanceTypeBoundUnion:
        return InstanceTypeBoundUnion.any()

    @classmethod
    def components(
            cls,
            domain: Type[DomainSpecifier[Instance[Data, Annotation]]]
    ) -> Tuple[Type[Component], ...]:
        # Import the base FromData component
        from ..component import ToData

        return ToData,
