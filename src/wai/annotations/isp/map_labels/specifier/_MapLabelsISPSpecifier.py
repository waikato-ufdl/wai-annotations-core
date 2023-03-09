from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import Data
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.classification import Classification
from ....domain.image.object_detection import DetectedObjects


class MapLabelsISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the map-labels ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Map Labels"

    @classmethod
    def description(cls) -> str:
        return "Maps object-detection labels from one set to another"

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
                f"MapLabels only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion((Data, Classification), (Data, DetectedObjects)),
            InstanceTypeBoundUnion((Data, Classification), (Data, DetectedObjects)),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(
            cls,
            bound_relationship: InstanceTypeBoundRelationship
    ) -> Tuple[Type[Component], ...]:
        from ..component import MapLabels
        return MapLabels,
