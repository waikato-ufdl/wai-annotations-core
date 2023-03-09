from ..domain import Instance
from ..stage.bounds import InstanceTypeBoundUnion
from ..stream import StreamProcessor, ThenFunction, DoneFunction
from ..stream.util import RequiresNoFinalisation
from .error import BadDomain


class InlineDomainValidator(
    RequiresNoFinalisation,
    StreamProcessor[Instance, Instance]
):
    """
    Makes sure all instances match the given type-bound.
    """
    def __init__(self, bound: InstanceTypeBoundUnion):
        self._bound = bound

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        instance_type = type(element)
        if self._bound.intersection_bound(InstanceTypeBoundUnion(instance_type)) is None:
            raise BadDomain(
                f"{instance_type.__qualname__} (instance-type for {instance_type.domain_specifier().name()}) "
                f"in stream where allowed instance-types are {self._bound}"
            )

        then(element)
