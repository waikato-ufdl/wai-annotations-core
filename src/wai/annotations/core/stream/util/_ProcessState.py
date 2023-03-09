from typing import TypeVar

from ...util import InstanceState

OwnerType = TypeVar('OwnerType')
StateType = TypeVar('StateType')


class ProcessState(InstanceState[StateType]):
    """
    Descriptor for stream processing state that automatically resets
    on each application of a pipeline.
    """
    def __delete__(self, instance: OwnerType):
        # Deleting an uninitialised process-state is a no-op
        if instance not in self._state:
            return

        super().__delete__(instance)
