from re import compile
from typing import Pattern, Optional, List

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption, FlagOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....core.util import InstanceState
from ....domain.image import ImageInstance
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.classification import ImageClassificationInstance
from ....domain.image.object_detection.util import get_object_label


class FilterLabels(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Processes a stream of image object-detection instances,
    filtering out labels.
    """
    # The labels that should be included in the output format.
    # If None, use regex matching (see below)
    labels = TypedOption("-l", "--labels",
                         type=str,
                         nargs="+",
                         help="labels to use")

    # The regex to use to select labels to include when an
    # explicit list of labels is not given
    regex = TypedOption("-r", "--regexp",
                        type=str,
                        metavar="regexp",
                        help="regular expression for using only a subset of labels")

    # The compiled regex
    _pattern: Optional[Pattern] = InstanceState(lambda self: compile(self.regex) if self.regex is not None else None)

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        if isinstance(element, ImageObjectDetectionInstance):
            # Use the options to filter the located objects by label
            self.remove_invalid_objects(element.annotations)
            # no annotations left? mark as negative
            if len(element.annotations) == 0:
                new_element = type(element)(element.data, None)
                then(new_element)
                return
        elif isinstance(element, ImageClassificationInstance):
            # mark as negative if label doesn't match
            if not self.filter_label(element.annotations.label):
                new_element = type(element)(element.data, None)
                then(new_element)
                return

        then(element)

    def remove_invalid_objects(self, located_objects: LocatedObjects):
        """
        Removes objects with labels that are not valid under the given options.

        :param located_objects:     The located objects to process.
        """
        # Create a list of objects to remove
        invalid_objects: List[int] = []

        # Search the located objects
        for index, located_object in enumerate(located_objects):
            if not self.filter_object(located_object):
                invalid_objects.append(index)

        # Remove the invalid objects
        for index in reversed(invalid_objects):
            located_objects.pop(index)

    def filter_label(self, label: str) -> bool:
        """
        Filter function which selects labels that match the given options.

        :param label:   The label to test.
        :return:        True if the label matches, false if not.
        """
        if len(self.labels) == 0 and self._pattern is None:
            return True
        elif len(self.labels) == 0:
            return bool(self._pattern.match(label))
        elif self._pattern is None:
            return label in self.labels
        else:
            return bool(self._pattern.match(label)) or label in self.labels

    def filter_object(self, located_object: LocatedObject) -> bool:
        """
        Filter function which selects objects whose labels match the given options.

        :param located_object:  The located object to test.
        :return:                True if the object matches, false if not.
        """
        # Filter the label
        return self.filter_label(get_object_label(located_object))
