from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier


class StripAnnotationsISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the strip-annotations inline stream-processor.
    """
    @classmethod
    def name(cls) -> str:
        return "Strip Annotations"

    @classmethod
    def description(cls) -> str:
        return "ISP which removes annotations from instances"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion.any(),
            InstanceTypeBoundUnion.any(),
            input_instance_type_must_match_output_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ..component import StripAnnotations
        return StripAnnotations,
