from abc import ABC


class RequiresNoFinalisation(ABC):
    """
    Mixin for stream processors/sinks which don't require finalisation.
    """
    def finish(self, *args, **kwargs):
        # Find the 'done' function if one is given
        done = (
            kwargs['done'] if 'done' in kwargs
            else args[1] if len(args) >= 2
            else None
        )

        # Call the 'done' function (it's idempotent so doesn't matter
        # if it has already been called)
        if done is not None:
            done()

    def __init_subclass__(cls, **kwargs):
        # Should only be used with processors/sinks
        from .._StreamProcessor import StreamProcessor
        from .._StreamSink import StreamSink

        if not issubclass(cls, (StreamProcessor, StreamSink)):
            raise Exception(
                f"{RequiresNoFinalisation.__qualname__} can only be used in conjunction "
                f"with {StreamProcessor.__qualname__} or {StreamSink.__qualname__}"
            )
