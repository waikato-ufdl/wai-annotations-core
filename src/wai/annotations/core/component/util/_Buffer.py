from typing import TypeVar, List

from wai.common.cli.options import TypedOption

from ...stream import ThenFunction, DoneFunction
from ...stream.util import ProcessState
from .._ProcessorComponent import ProcessorComponent

ElementType = TypeVar("ElementType")


class Buffer(ProcessorComponent[ElementType, List[ElementType]]):
    """
    Utility component which buffers the stream into lists of elements.

    The chunk_size option determines how many items will be buffered
    before a list if forwarded. If chunk_size is not strictly positive,
    no chunking is performed, and the entire stream of items will be
    buffered before forwarding. Either way, an empty list will be forwarded
    if no items are received.
    """
    chunk_size: int = TypedOption(
        "-c", "--chunk-size",
        type=int,
        default=0,
        help="the number of items to buffer before forwarding",
        metavar="SIZE"
    )

    # The buffered elements
    _buffer: List[ElementType] = ProcessState(lambda self: [])

    # Whether any chunks have been sent
    _any_sent: bool = ProcessState(lambda self: False)

    def process_element(self, element: ElementType, then: ThenFunction[List[ElementType]], done: DoneFunction):
        # Add the element to the buffer
        self._buffer.append(element)

        # Forward the buffer if chunking is enabled
        if self.chunk_size > 0 and len(self._buffer) == self.chunk_size:
            then(self._buffer)
            self._buffer = []
            self._any_sent = True

    def finish(self, then: ThenFunction[List[ElementType]], done: DoneFunction):
        # If nothing has been forwarded yet, or the buffer has remaining items,
        # forward whatever is buffered, even if the buffer is empty
        if not self._any_sent or len(self._buffer) != 0:
            then(self._buffer)

        done()
