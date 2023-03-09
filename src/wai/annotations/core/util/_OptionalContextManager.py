from typing import ContextManager, Optional, TypeVar

# The type of the managed context-manager
ManagedType = TypeVar("ManagedType")


class OptionalContextManager(ContextManager[Optional[ManagedType]]):
    """
    A context manager that optional returns a context of a given type.
    """
    def __init__(self, context_manager: Optional[ContextManager[ManagedType]]):
        self._context_manager = context_manager

    def __enter__(self):
        if self._context_manager is None:
            return None

        return self._context_manager.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._context_manager is not None:
            self._context_manager.__exit__(exc_type, exc_val, exc_tb)
