from typing import Optional, Dict, Union

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....core.util import InstanceState
from ....domain.classification import Classification
from ....domain.image.object_detection import DetectedObjects
from ....domain.image.object_detection.util import get_object_label, set_object_label


def _label_table_init(self: 'MapLabels') -> Dict[str, str]:
    label_table = {}
    for map_string in self.label_mapping:
        old, new = map_string.split("=")

        # Make sure we don't double-map a label
        if old in label_table:
            raise ValueError(
                f"Multiple mappings specified for label '{old}': {label_table[old]}, {new}"
            )

        label_table[old] = new

    return label_table

class MapLabels(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Data, Union[Classification, DetectedObjects]],
        Instance[Data, Union[Classification, DetectedObjects]]
    ]
):
    """
    Processes a stream of object-detection instances, mapping labels
    from one set to another.
    """
    label_mapping = TypedOption(
        "-m", "--mapping",
        type=str,
        metavar="old=new", action='concat',
        help="mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)"
    )

    label_table: Dict[str, str] = InstanceState(_label_table_init)

    def process_element(
            self,
            element: Instance[Data, Union[Classification, DetectedObjects]],
            then: ThenFunction[Instance[Data, Union[Classification, DetectedObjects]]],
            done: DoneFunction
    ):
        # Get the annotation
        annotation = element.annotation

        # Can't map unannotated instances
        if annotation is None:
            then(element)

        if isinstance(annotation, Classification):
            then(
                type(element).from_parts(
                    element.key,
                    element.data,
                    Classification(self.label_table.get(annotation.label, annotation.label))
                )
            )

        self.apply_label_mapping(annotation)
        then(element)

    def apply_label_mapping(self, located_objects: LocatedObjects):
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param located_objects:     The parsed objects
        """
        # Do nothing if no mapping provided
        if len(self.label_table) == 0:
            return

        # Process each object
        for located_object in located_objects:
            # Get the object's current label
            label: Optional[str] = get_object_label(located_object, None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self.label_table:
                set_object_label(located_object, self.label_table[label])
