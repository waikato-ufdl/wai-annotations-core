from typing import Callable, Dict, Generic, Optional, Type, TypeVar, TYPE_CHECKING

from .....stream.util import ProcessState

if TYPE_CHECKING:
    from .....component.util.output.splitting import SplitSink


SplitSinkType = TypeVar("SplitSinkType", bound='SplitSink')
StateType = TypeVar("StateType")
SelfType = TypeVar("SelfType", bound='SplitState')


class SplitState(Generic[SplitSinkType, StateType]):
    """
    Class that initialises state for each individual split.
    """
    def __init__(
            self,
            instance: SplitSinkType,
            initialiser: Callable[[SplitSinkType], StateType]
    ):
        self._instance: SplitSinkType = instance
        self._initialiser: Callable[[SplitSinkType], StateType] = initialiser
        self._split_states: Dict[str, StateType] = {}

    @classmethod
    def as_process_state(
            cls: Type[SelfType],
            initialiser: Callable[[SplitSinkType], StateType]
    ) -> ProcessState['SplitState[SplitSinkType, StateType]']:
        return ProcessState(lambda self: cls(self, initialiser))

    @property
    def current_split_label(self) -> Optional[str]:
        return self._instance.split_label

    @property
    def current_split_is_initialised(self) -> bool:
        return self.current_split_label in self._split_states

    @property
    def for_current_split(self) -> StateType:
        # Get the current split label
        split_label = self.current_split_label

        # Initialise the state for this split if not already
        if not self.current_split_is_initialised:
            self._split_states[split_label] = self._initialiser(self._instance)

        return self._split_states[split_label]

    @for_current_split.setter
    def for_current_split(self, value: StateType):
        # Get the current split label
        split_label = self.current_split_label

        self._split_states[split_label] = value

    @for_current_split.deleter
    def for_current_split(self):
        # Get the current split label
        split_label = self.current_split_label

        del self._split_states[split_label]
