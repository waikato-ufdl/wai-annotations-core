from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier


class RemoveClassesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the remove-classes inline stream-processor.
    """
    @classmethod
    def name(cls) -> str:
        return "Remove Classes"

    @classmethod
    def description(cls) -> str:
        return "Removes classes from classification/image-segmentation instances"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.classification import Classification
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        if (
                input_domain is ImageSegmentationDomainSpecifier or
                input_domain.annotations_type() is Classification
        ):
            return input_domain

        raise Exception("RemovesClasses handles image segmentation and classification domains only")

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        from ....core.domain import Data
        from ....domain.classification import Classification
        from ....domain.image.segmentation import ImageSegmentationAnnotation
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion((Data, Classification), (Data, ImageSegmentationAnnotation)),
            InstanceTypeBoundUnion((Data, Classification), (Data, ImageSegmentationAnnotation)),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ..component import RemoveClasses
        return RemoveClasses,
