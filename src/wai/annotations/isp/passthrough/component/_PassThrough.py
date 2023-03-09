from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Data, Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation


class PassThrough(
    RequiresNoFinalisation,
    ProcessorComponent[
        Instance[Data, Annotation],
        Instance[Data, Annotation]
    ]
):
    """
    Inline stream-processor which does nothing to the stream.
    """
    def process_element(
            self,
            element: Instance[Data, Annotation],
            then: ThenFunction[Instance[Data, Annotation]],
            done: DoneFunction
    ):
        then(element)
