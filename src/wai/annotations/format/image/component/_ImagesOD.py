from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.image import Image
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance


class ImagesOD(AnnotationFileProcessor[ImageObjectDetectionInstance]):
    """
    Dummy reader that turns a list of images into an object detection dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[ImageObjectDetectionInstance]):
        then(
            ImageObjectDetectionInstance(
                Image.from_file(filename),
                LocatedObjects()
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[ImageObjectDetectionInstance]):
        then(
            ImageObjectDetectionInstance(
                Image.from_file(filename),
                None
            )
        )
