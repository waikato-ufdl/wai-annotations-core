from typing import Callable, ContextManager, TypeVar

from ._ProcessState import ProcessState
from ...util import ReentrantContextManager

ResourceType = TypeVar('ResourceType')
OwnerType = TypeVar("OwnerType")


class ProcessResource(
    ProcessState[ContextManager[ResourceType]]
):
    """
    Process-state which manages a resource.
    """
    def __init__(
            self,
            initialiser: Callable[[OwnerType], ContextManager[ResourceType]]
    ):
        # Creates a re-entrant variation on the context-manager provided
        def reentrant_initialiser(owner: OwnerType) -> ReentrantContextManager[ResourceType]:
            return ReentrantContextManager(initialiser(owner))

        super().__init__(reentrant_initialiser)

    def __set__(self, instance: OwnerType, value: ContextManager[ResourceType]):
        self.__delete__(instance)
        super().__set__(instance, ReentrantContextManager(value))

    def __delete__(self, instance: OwnerType):
        if instance in self._state:
            state = self._state[instance]
            assert isinstance(state, ReentrantContextManager)
            state.finish()

        super().__delete__(instance)
