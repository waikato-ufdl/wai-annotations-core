from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Data, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation


class DiscardNegatives(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Data, Annotation],
        Instance[Data, Annotation]
    ]
):
    """
    ISP which removes negatives from the stream.
    """
    def process_element(
            self,
            element: Instance[Data, Annotation],
            then: ThenFunction[Instance[Data, Annotation]],
            done: DoneFunction
    ):
        if element.is_unannotated:
            return

        then(element)
