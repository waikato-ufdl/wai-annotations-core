from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image import Image, ImageFormat


class ConvertImageFormat(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Image, Annotation],
        Instance[Image, Annotation]
    ]
):
    """
    Processes a stream of image-based instances, converting the
    image format to a specified type.
    """
    format = TypedOption(
        "-f", "--format",
        type=ImageFormat,
        required=True,
        metavar="FORMAT",
        help="format to convert images to"
    )

    def process_element(
            self,
            element: Instance[Image, Annotation],
            then: ThenFunction[Instance[Image, Annotation]],
            done: DoneFunction
    ):
        then(
            element.from_parts(
                element.key,
                element.data.convert(self.format),
                element.annotation
            )
        )
