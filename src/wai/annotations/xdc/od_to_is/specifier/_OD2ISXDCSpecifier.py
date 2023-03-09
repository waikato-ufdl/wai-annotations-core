from typing import Tuple, Type

from ....core.component import Component
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier, ImageObjectDetectionInstance
from ....domain.image.segmentation import ImageSegmentationDomainSpecifier, ImageSegmentationInstance


class OD2ISXDCSpecifier(ProcessorStageSpecifier):
    """
    Specifies the image object-detection -> image segmentation
    cross-domain converter.
    """
    @classmethod
    def name(cls) -> str:
        return "OD -> IS"

    @classmethod
    def description(cls) -> str:
        return "Converts image object-detection instances into image segmentation instances"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            ImageObjectDetectionInstance,
            ImageSegmentationInstance
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[Component], ...]:
        from ..component import OD2ISXDC
        return OD2ISXDC,
