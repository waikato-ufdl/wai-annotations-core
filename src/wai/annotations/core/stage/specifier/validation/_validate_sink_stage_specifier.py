from typing import Any, Type

from ....plugin.specifier.validation import validate_plugin_specifier
from ...bounds import InstanceTypeBoundUnion
from .._SinkStageSpecifier import SinkStageSpecifier


def validate_sink_stage_specifier(
        specifier: Any
) -> Type[SinkStageSpecifier]:
    """
    Validates a sink-stage specifier.
    """
    source_stage_specifier, class_method_return_values = validate_plugin_specifier(
        specifier,
        SinkStageSpecifier,
        **{
            SinkStageSpecifier.bound.__name__: InstanceTypeBoundUnion
        }
    )

    return source_stage_specifier
