from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.classification import Classification
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.classification import ImageClassificationInstance


class ImagesIC(AnnotationFileProcessor[ImageClassificationInstance]):
    """
    Dummy reader that turns a list of images into an image classification dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[ImageClassificationInstance]):
        then(
            ImageClassificationInstance(
                Image.from_file(filename),
                Classification("?")
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[ImageClassificationInstance]):
        then(
            ImageClassificationInstance(
                Image.from_file(filename),
                None
            )
        )
