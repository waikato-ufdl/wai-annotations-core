from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier, ImageObjectDetectionInstance


class FilterMetadataISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the filter-labels ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Filter Metadata"

    @classmethod
    def description(cls) -> str:
        return "Filters detected objects based on their meta-data."

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            ImageObjectDetectionInstance,
            ImageObjectDetectionInstance
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...filter_metadata.component import FilterMetadata
        return FilterMetadata,
