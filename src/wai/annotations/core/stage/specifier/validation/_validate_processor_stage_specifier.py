from typing import Any, Type

from .._ProcessorStageSpecifier import ProcessorStageSpecifier
from ....component import ProcessorComponent, SourceComponent
from ....plugin.specifier.validation import validate_plugin_specifier
from ...bounds import InstanceTypeBoundRelationship
from .._SourceStageSpecifier import SourceStageSpecifier
from ....util import describe_value, is_subtype


def validate_processor_stage_specifier(
        specifier: Any
) -> Type[ProcessorStageSpecifier]:
    """
    Validates a processor-stage specifier.
    """
    processor_stage_specifier, class_method_return_values = validate_plugin_specifier(
        specifier,
        ProcessorStageSpecifier,
        **{
            ProcessorStageSpecifier.bound_relationship.__name__: InstanceTypeBoundRelationship
        }
    )

    return processor_stage_specifier
