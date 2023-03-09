from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Data
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.classification import Classification
from ....domain.image.object_detection import DetectedObjects
from ....domain.image.segmentation import ImageSegmentationAnnotation


class WriteLabelsISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the write-labels inline stream-processor.
    """
    @classmethod
    def name(cls) -> str:
        return "Write Labels"

    @classmethod
    def description(cls) -> str:
        return "ISP which gathers labels and writes them to disk"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion(
                (Data, Classification),
                (Data, DetectedObjects),
                (Data, ImageSegmentationAnnotation)
            ),
            InstanceTypeBoundUnion.any(),
            input_instance_type_must_match_output_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ..component import WriteLabels
        return WriteLabels,
