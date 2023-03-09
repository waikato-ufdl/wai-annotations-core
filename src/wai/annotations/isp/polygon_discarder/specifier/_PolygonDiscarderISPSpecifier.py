from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image.object_detection import ImageObjectDetectionInstance


class PolygonDiscarderISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the dimension-discarder.
    """
    @classmethod
    def name(cls) -> str:
        return "Polygon Discarder"

    @classmethod
    def description(cls) -> str:
        return "Removes annotations with polygons which fall outside certain point limit constraints"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            ImageObjectDetectionInstance,
            ImageObjectDetectionInstance,
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...polygon_discarder.component import PolygonDiscarder
        return PolygonDiscarder,
