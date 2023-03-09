from abc import abstractmethod

from wai.common.adams.imaging.locateobjects import LocatedObject

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import DetectedObjects


class Coercion(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Data, DetectedObjects],
        Instance[Data, DetectedObjects]
    ]
):
    """
    Base class for all coercions.
    """
    def process_element(
            self,
            element: Instance[Data, DetectedObjects],
            then: ThenFunction[Instance[Data, DetectedObjects]],
            done: DoneFunction
    ):
        # Get the located objects from the instance
        located_objects = element.annotation

        # Process each located object
        if located_objects is not None:
            for located_object in located_objects:
                self._process_located_object(located_object)

        then(element)

    @abstractmethod
    def _process_located_object(self, located_object: LocatedObject):
        """
        Handles the processing of individual located objects.

        :param located_object:  The located object to coerce.
        """
        pass
