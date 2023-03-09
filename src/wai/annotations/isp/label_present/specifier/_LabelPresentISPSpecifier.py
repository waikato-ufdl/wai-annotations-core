from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image.object_detection import ImageObjectDetectionInstance


class LabelPresentISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the labels-in-region ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Label Present"

    @classmethod
    def description(cls) -> str:
        return "Keeps or discards images depending on whether annotations with certain label(s) are present. " \
               "Checks can be further tightened by defining regions in the image that annotations must overlap with (or not overlap at all)."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return ImageObjectDetectionDomainSpecifier
        else:
            raise Exception(
                f"LabelPresent only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

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
        from ...label_present.component import LabelPresent
        return LabelPresent,
