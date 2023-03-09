from ....core.component import SinkComponent
from ....core.domain import Annotation, Data, Instance
from ....core.stream.util import RequiresNoFinalisation


class ToVoid(
    RequiresNoFinalisation,
    SinkComponent[Instance[Data, Annotation]]
):
    """
    Consumes instances by discarding them.
    """
    def consume_element(self, element: Instance[Data, Annotation]):
        pass
