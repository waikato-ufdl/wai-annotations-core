from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image.object_detection import DetectedObjects


class DimensionDiscarderISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the dimension-discarder.
    """
    @classmethod
    def name(cls) -> str:
        return "Dimension Discarder"

    @classmethod
    def description(cls) -> str:
        return "Removes annotations which fall outside certain size constraints"

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
                f"DimensionDiscarder only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

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
        from ...dimension_discarder.component import DimensionDiscarder
        return DimensionDiscarder,
