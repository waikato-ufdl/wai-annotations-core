from wai.common.cli.options import FlagOption

from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image import Image


class DiscardInvalidImages(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Image, Annotation],
        Instance[Image, Annotation]
    ]
):
    """
    Processes a stream of image-based instances, discarding invalid images
    (e.g. corrupt files or annotations with not file attached).
    """

    verbose = FlagOption(
        "-v", "--verbose",
        help="whether to output debugging information"
    )

    def process_element(
            self,
            element: Instance[Image, Annotation],
            then: ThenFunction[Instance[Image, Annotation]],
            done: DoneFunction
    ):
        # no data?
        if (element.data is None) or (len(element.data.data) == 0):
            if self.verbose:
                self.logger.info("No image data, skipping!")
            return

        # try reading the data
        try:
            element.data.pil_image
        except:
            if self.verbose:
                self.logger.info("Failed to read image data, skipping!")
            return

        then(element)
