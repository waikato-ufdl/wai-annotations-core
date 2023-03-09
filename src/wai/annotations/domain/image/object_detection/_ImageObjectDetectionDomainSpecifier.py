from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ._ImageObjectDetectionInstance import ImageObjectDetectionInstance

DESCRIPTION = """Images containing multiple identified objects.

The image object-detection domain pertains to finding regions of still images which contain identifiable objects.
Instances in this domain consist of an image and a set of regions (either axis-aligned boxes or polygons), each with
an accompanying label, identifying the detected objects within the image.
"""


class ImageObjectDetectionDomainSpecifier(DomainSpecifier[ImageObjectDetectionInstance]):
    """
    Domain specifier for images annotated with objects
    detected within those images.
    """
    @classmethod
    def name(cls) -> str:
        return "Image Object-Detection Domain"

    @classmethod
    def description(cls) -> str:
        return DESCRIPTION

    @classmethod
    def instance_type(cls) -> Type[ImageObjectDetectionInstance]:
        return ImageObjectDetectionInstance
