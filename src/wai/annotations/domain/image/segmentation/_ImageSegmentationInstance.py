from typing import Type, Optional, TypeVar

from ....core.domain.specifier import DomainSpecifier
from ....core.util.path import PathKeyLike
from .._Image import Image
from .._ImageInstance import ImageInstance
from ._ImageSegmentationAnnotation import ImageSegmentationAnnotation

SelfType = TypeVar("SelfType", bound='ImageSegmentationInstance')


class ImageSegmentationInstance(ImageInstance[ImageSegmentationAnnotation]):
    """
    An item in an image-segmentation data-set.
    """
    def __init__(
            self,
            key: PathKeyLike,
            data: Optional[Image],
            annotations: Optional[ImageSegmentationAnnotation]
    ):
        # Make sure the data and annotation images are the same size
        if data is not None and annotations is not None and data.size != annotations.size:
            raise Exception(f"Image size {data.size} does not match segments size {annotations.size}")

        super().__init__(key, data, annotations)

    @classmethod
    def domain_specifier(cls: Type[SelfType]) -> Type['DomainSpecifier[SelfType]']:
        from ._ImageSegmentationDomainSpecifier import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

    @classmethod
    def annotation_type(cls) -> Type[ImageSegmentationAnnotation]:
        return ImageSegmentationAnnotation
