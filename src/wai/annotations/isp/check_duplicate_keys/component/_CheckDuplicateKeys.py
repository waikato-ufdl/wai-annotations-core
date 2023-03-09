from typing import Set

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation, ProcessState
from ....core.domain import Annotation, Data, Instance


class CheckDuplicateKeys(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Data, Annotation],
        Instance[Data, Annotation]
    ]
):
    """
    Processes a stream of instances ensuring that the same
    key doesn't appear twice.
    """
    # The set of keys we've already seen
    _seen: Set[str] = ProcessState(lambda self: set())

    def process_element(
            self,
            element: Instance[Data, Annotation],
            then: ThenFunction[Instance[Data, Annotation]],
            done: DoneFunction
    ):
        # Get the key from the element
        key = str(element.key)

        # If we've seen it, raise an error
        if key in self._seen:
            raise ValueError(f"Instance '{key}' appeared multiple times during conversion")

        # Add the key to the set of seen keys
        self._seen.add(key)

        then(element)
