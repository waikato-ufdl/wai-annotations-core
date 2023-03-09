from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ._ImageClassificationInstance import ImageClassificationInstance

DESCRIPTION = """Images categorised by content.

The image classification domain deals with labelling entire images as containing a certain subject. Instances in this
domain contain an image and a string label classifying the image.
"""


class ImageClassificationDomainSpecifier(DomainSpecifier[ImageClassificationInstance]):
    """
    Domain specifier for images annotated with a label
    classifying the contents of the image
    """
    @classmethod
    def name(cls) -> str:
        return "Image Classification Domain"

    @classmethod
    def description(cls) -> str:
        return DESCRIPTION

    @classmethod
    def instance_type(cls) -> Type[ImageClassificationInstance]:
        return ImageClassificationInstance
