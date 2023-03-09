from ....core.component import ProcessorComponent
from ....core.component.util import WithPossiblySeededRandomness
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from wai.common.cli.options import TypedOption


class Sample(
    RequiresNoFinalisation,
    WithPossiblySeededRandomness,
    ProcessorComponent[Instance, Instance]
):
    """
    ISP that selects a sub-sample from the stream.
    """
    threshold: float = TypedOption(
        "-T", "--threshold",
        type=float,
        default=0.0,
        help="the threshold to use for Random.rand(): if equal or above, sample gets selected; range: 0-1; default: 0 (= always)"
    )

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        if (self.threshold < 0) or (self.threshold > 1):
            raise Exception(f"Threshold must be between 0 and 1 (inclusive), supplied: {self.threshold}")

        if self.threshold == 1.0:
            then(element)
            return
        elif self.threshold == 0.0:
            return

        if self.random.random() >= self.threshold:
            then(element)

