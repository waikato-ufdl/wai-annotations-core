from typing import Type, TypeVar

from ....core.domain.specifier import DomainSpecifier
from .._ImageInstance import ImageInstance
from .util import render_annotations_onto_image
from ._DetectedObjects import DetectedObjects

SelfType = TypeVar("SelfType", bound='ImageObjectDetectionInstance')


class ImageObjectDetectionInstance(ImageInstance[DetectedObjects]):
    """
    Adds the _repr_png_ method dynamically to object-detection instances.
    """
    @classmethod
    def annotation_type(cls) -> Type[DetectedObjects]:
        return DetectedObjects

    @classmethod
    def domain_specifier(cls: Type[SelfType]) -> Type['DomainSpecifier[SelfType]']:
        from ._ImageObjectDetectionDomainSpecifier import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    def __getattribute__(self, item):
        if item == '_repr_png_' and self.file_info.data is not None:
            return lambda: render_annotations_onto_image(self._file_info.data, self._annotations)

        return super().__getattribute__(item)
