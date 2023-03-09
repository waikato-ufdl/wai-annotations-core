from ...plugin.names import StagePluginName
from ...stage.bounds import InstanceTypeBoundUnion


class StageInvalidForOutputBounds(Exception):
    """
    Error for when an attempt is made to add a stage to the
    conversion pipeline which doesn't accept instances of
    the types it might receive.
    """
    def __init__(
            self,
            stage_name: StagePluginName,
            stage_input_bounds: InstanceTypeBoundUnion,
            current_output_bounds: InstanceTypeBoundUnion
    ):
        super().__init__(
                f"Stage '{stage_name}' has input-bound {stage_input_bounds} "
                f"which is incompatible with the output bounds at this stage ({current_output_bounds})"
        )
