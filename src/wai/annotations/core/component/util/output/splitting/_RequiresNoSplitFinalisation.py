from abc import ABC


class RequiresNoSplitFinalisation(ABC):
    """
    Mixin class for declaring that a SplitSink doesn't need to
    finalise its splits.
    """
    def finish_split(self):
        pass

    def __init_subclass__(cls, **kwargs):
        # Should only be used with split-sinks
        from ._SplitSink import SplitSink

        if not issubclass(cls, SplitSink):
            raise Exception(
                f"{RequiresNoSplitFinalisation.__qualname__} can only be used in conjunction "
                f"with {SplitSink.__qualname__}"
            )
