from abc import ABC, abstractmethod
from typing import Dict, Optional, Type, TypeVar

from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.classification import Classification
from ....domain.image.object_detection import DetectedObjects, ImageObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label

DataType = TypeVar('DataType', bound=Data)
ClassificationInstanceType = TypeVar(
    'ClassificationInstanceType',
    bound=Instance[Data, Classification]  # Should be Instance[DataType, Classification], but Python can't handle this
)

class OD2ICXDC(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Data, DetectedObjects],
        ClassificationInstanceType
    ],
    ABC
):
    """
    Cross-domain converter from the image object-detection domain to the
    image classification domain.
    """
    multiplicity_method: str = TypedOption(
        "-m", "--multiplicity",
        type=str,
        choices=["error", "majority", "single", "skip"],
        default="error",
        help="how to handle instances with more than one located object",
        metavar="HANDLER"
    )

    @classmethod
    @abstractmethod
    def output_type(cls) -> Type[ClassificationInstanceType]:
        raise NotImplementedError()

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ClassificationInstanceType],
            done: DoneFunction
    ):
        # Get the located objects from the instance
        objects = element.annotation

        # If the instance is a negative, leave it as one
        if objects is None or len(objects) == 0:
            return then(
                self.output_type().from_parts(element.key, element.data, None)
            )

        if len(objects) > 1:
            if self.multiplicity_method == "error":
                raise Exception(f"More than one detected object for {element.key}")
            elif self.multiplicity_method == "skip":
                return
            elif self.multiplicity_method == "single":
                unique_labels = set(
                    get_object_label(object, None)
                    for object in objects
                )
                if len(unique_labels) > 1:
                    raise Exception(f"More than one type of detected object for {element.key}")
                label = unique_labels.pop()
            elif self.multiplicity_method == "majority":
                labels_to_counts: Dict[Optional[str], int] = {}
                for object in objects:
                    label = get_object_label(object, None)
                    if label not in labels_to_counts:
                        labels_to_counts[label] = 0
                    if label is not None:
                        labels_to_counts[label] += 1
                label = max(labels_to_counts.keys(), key=labels_to_counts.get)
            else:
                raise NotImplementedError(f"Unknown multiplicity_method option '{self.multiplicity_method}'")
        else:  # len(objects) == 1
            label = get_object_label(objects[0], None)

        then(
            self.output_type().from_parts(
                element.key,
                element.data,
                Classification(label) if label is not None else None
            )
        )
