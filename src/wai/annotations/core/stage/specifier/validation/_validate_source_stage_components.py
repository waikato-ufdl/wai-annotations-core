from typing import Any, Tuple

from ....component import SourceComponent, ProcessorComponent
from ....util import describe_value, is_subtype


def validate_source_stage_components(
        components: Any
) -> Tuple[SourceComponent, Tuple[ProcessorComponent, ...]]:
    """
    Validates the components of a source-stage specifier.
    """
    if not isinstance(components, tuple):
        raise TypeError("Components should be a tuple")

    if len(components) == 0:
        raise Exception("No components specified")

    # Make sure the first component is a source, and subsequent components are processors
    if not is_subtype(components[0], SourceComponent):
        raise Exception(f"Source stage must begin with source component, not {describe_value(components[0])}")
    for index, component in enumerate(components[1:]):
        if not is_subtype(component, ProcessorComponent):
            raise Exception(
                f"All subsequent components of a source stage must be processors, "
                f"element {index + 1} is {describe_value(component)}"
            )

    return components[0], components[1:]
