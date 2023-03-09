from typing import Any, Type

from ....plugin.specifier.validation import validate_plugin_specifier
from ...bounds import InstanceTypeBoundUnion
from .._SourceStageSpecifier import SourceStageSpecifier


def validate_source_stage_specifier(
        specifier: Any
) -> Type[SourceStageSpecifier]:
    """
    Validates a source-stage specifier.
    """
    source_stage_specifier, class_method_return_values = validate_plugin_specifier(
        specifier,
        SourceStageSpecifier,
        **{
            SourceStageSpecifier.bound.__name__: InstanceTypeBoundUnion
        }
    )

    return source_stage_specifier
