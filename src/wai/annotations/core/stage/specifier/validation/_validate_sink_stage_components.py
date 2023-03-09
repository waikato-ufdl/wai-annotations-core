from typing import Any, Tuple

from wai.annotations.core.component import ProcessorComponent, SinkComponent
from wai.annotations.core.util import describe_value, is_subtype


def validate_sink_stage_components(
        components: Any
) -> Tuple[Tuple[ProcessorComponent, ...], SinkComponent]:
    """
    Validates the components of a sink stage.
    """
    if not isinstance(components, tuple):
        raise TypeError("Components should be a tuple")

    if len(components) == 0:
        raise Exception("No components specified")

    for index, component in enumerate(components[:-1]):
        if not is_subtype(component, ProcessorComponent):
            raise Exception(
                f"All preceding components of a sink stage must be processors, "
                f"element {index} is {describe_value(component)}"
            )
    if not is_subtype(components[-1], SinkComponent):
        raise Exception(f"Sink stage must end with sink component, not {describe_value(components[-1])}")

    return components[:-1], components[-1]
