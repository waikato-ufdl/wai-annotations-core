from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.image.segmentation import ImageSegmentationAnnotation
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance


class ImagesIS(AnnotationFileProcessor[ImageSegmentationInstance]):
    """
    Dummy reader that turns a list of images into an image segmentation dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[ImageSegmentationInstance]):
        data = Image.from_file(filename)
        then(
            ImageSegmentationInstance(
                data,
                ImageSegmentationAnnotation(labels=[], size=data.size)
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[ImageSegmentationInstance]):
        then(
            ImageSegmentationInstance(
                Image.from_file(filename),
                None
            )
        )
