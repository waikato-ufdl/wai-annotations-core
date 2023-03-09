from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ._ImageSegmentationInstance import ImageSegmentationInstance

DESCRIPTION = """Images segmented by category.

The image segmentation domain 'colourises' an image by assigning a category to each pixel (where no category
corresponds to 'the background'). Instances in this domain are a still image and a corresponding table of the same
size, where each element is a label.
"""


class ImageSegmentationDomainSpecifier(DomainSpecifier[ImageSegmentationInstance]):
    """
    Domain specifier for images annotated with a label for each
    pixel in the image.
    """
    @classmethod
    def name(cls) -> str:
        return "Image Segmentation Domain"

    @classmethod
    def description(cls) -> str:
        return DESCRIPTION

    @classmethod
    def instance_type(cls) -> Type[ImageSegmentationInstance]:
        return ImageSegmentationInstance
