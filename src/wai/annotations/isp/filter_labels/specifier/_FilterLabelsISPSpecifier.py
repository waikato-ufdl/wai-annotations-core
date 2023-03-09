from typing import Type, Tuple, Union

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.classification import Classification
from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier, ImageObjectDetectionInstance


class FilterLabelsISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the filter-labels ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Filter Labels"

    @classmethod
    def description(cls) -> str:
        return "Filters detected objects down to those with specified labels or, "\
               "in case of image classification, removes the label if it doesn't match."

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion((Data, Classification), ImageObjectDetectionInstance),
            InstanceTypeBoundUnion((Data, Classification), ImageObjectDetectionInstance),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )


    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...filter_labels.component import FilterLabels
        return FilterLabels,
