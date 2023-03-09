from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ...classification import Classification
from .._ImageInstance import ImageInstance


class ImageClassificationInstance(ImageInstance[Classification]):
    """
    An item in an image-classification data-set.
    """

    @classmethod
    def domain_specifier(cls: Type['ImageClassificationInstance']) -> Type['DomainSpecifier[ImageClassificationInstance]']:
        from ._ImageClassificationDomainSpecifier import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

    @classmethod
    def annotation_type(cls) -> Type[Classification]:
        return Classification
