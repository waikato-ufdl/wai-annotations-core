from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.image import Image


class ConvertImageFormatISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the convert-image-format ISP.
    """
    @classmethod
    def name(cls) -> str:
        return "Convert Image Format"

    @classmethod
    def description(cls) -> str:
        return "Converts images from one format to another"

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
        from ...convert_image_format.component import ConvertImageFormat
        return ConvertImageFormat,
