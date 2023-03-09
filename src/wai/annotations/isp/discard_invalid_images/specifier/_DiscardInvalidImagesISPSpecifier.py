from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image import Image


class DiscardInvalidImagesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the discard-invalid-images ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Discard Invalid Images"

    @classmethod
    def description(cls) -> str:
        return "Discards images that cannot be loaded (e.g., corrupt image file or annotations with no image)"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            (Image, Annotation),
            (Image, Annotation),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...discard_invalid_images.component import DiscardInvalidImages
        return DiscardInvalidImages,
