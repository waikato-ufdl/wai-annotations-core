from typing import Type, Tuple

from ....core.component import Component, ProcessorComponent
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier


class PassThroughISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the pass-through inline stream-processor.
    """
    @classmethod
    def name(cls) -> str:
        return "Passthrough"

    @classmethod
    def description(cls) -> str:
        return "Dummy ISP which has no effect on the conversion stream"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion.any(),
            InstanceTypeBoundUnion.any(),
            input_instance_type_must_match_output_instance_type=True
        )


    @classmethod
    def components(
            cls,
            bound_relationship: InstanceTypeBoundRelationship
    ) -> Tuple[Type[Component], ...]:
        from ...passthrough.component import PassThrough
        return PassThrough,
