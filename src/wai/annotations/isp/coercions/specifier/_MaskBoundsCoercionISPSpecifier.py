from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image.object_detection import DetectedObjects


class MaskBoundsCoercionISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the mask-bounds coercion.
    """
    @classmethod
    def name(cls) -> str:
        return "Mask Bounds Coercion"

    @classmethod
    def description(cls) -> str:
        return "Converts all annotation bounds into polygon regions"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            (Data, DetectedObjects),
            (Data, DetectedObjects),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...coercions.component import MaskBoundsCoercion
        return MaskBoundsCoercion,
