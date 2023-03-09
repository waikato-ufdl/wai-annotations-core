from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier


class DiscardNegativesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the discard-negatives ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Discard Negatives"

    @classmethod
    def description(cls) -> str:
        return "Discards negative examples (those without annotations) from the stream"


    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            (Data, Annotation),
            (Data, Annotation),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )


    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ..component import DiscardNegatives
        return DiscardNegatives,
