from typing import Any, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.util import describe_value, is_subtype


def validate_processor_stage_components(
        components: Any
) -> Tuple[ProcessorComponent, ...]:
    """
    Validates the components of a processor stage.
    """
    if not isinstance(components, tuple):
        raise TypeError("Components should be a tuple")

    if len(components) == 0:
        raise Exception("No components specified")

    # Make sure all components are processors
    for index, component in enumerate(components):
        if not is_subtype(component, ProcessorComponent):
            raise Exception(
                f"Processor stage can only consist of processor components, "
                f"element {index} is {describe_value(component)}"
            )

    return components
