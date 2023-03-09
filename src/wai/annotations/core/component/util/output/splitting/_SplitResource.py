from contextlib import ExitStack
from typing import Callable, ContextManager, Generic, Type, TypeVar, TYPE_CHECKING

from .....stream.util import ProcessResource
from .....util import ReentrantContextManager
from ._SplitState import SplitState

if TYPE_CHECKING:
    from ._SplitSink import SplitSink

SplitSinkType = TypeVar("SplitSinkType", bound='SplitSink')
ResourceType = TypeVar("ResourceType")
SelfType = TypeVar("SelfType", bound='SplitResource')


class SplitResource(
    ContextManager[ResourceType],
    Generic[SplitSinkType, ResourceType]
):
    def __init__(
            self,
            instance: SplitSinkType,
            initialiser: Callable[[SplitSinkType], ContextManager[ResourceType]]
    ):
        self._exit_stack: ExitStack = ExitStack()

        def initialise_and_add_to_exit_stack(sink: SplitSinkType) -> ReentrantContextManager[ResourceType]:
            resource_context_manager = ReentrantContextManager(initialiser(sink))
            self._exit_stack.enter_context(resource_context_manager)
            return resource_context_manager

        self._split_state: SplitState[SplitSinkType, ReentrantContextManager[ResourceType]] = (
            SplitState(instance, initialise_and_add_to_exit_stack)
        )

    @classmethod
    def as_process_resource(
            cls: Type[SelfType],
            initialiser: Callable[[SplitSinkType], ContextManager[ResourceType]]
    ) -> ProcessResource[SelfType]:
        return ProcessResource(lambda self: cls(self, initialiser))

    def __enter__(self) -> ResourceType:
        with self._split_state.for_current_split as resource:
            return resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._exit_stack.__exit__(exc_type, exc_val, exc_tb)
