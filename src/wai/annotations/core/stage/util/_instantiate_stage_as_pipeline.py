from typing import Tuple, Type, TYPE_CHECKING

from wai.common.cli import OptionsList

from ...component import *
from ...stream import Pipeline
from ._get_configured_stage_parser import get_configured_stage_parser

if TYPE_CHECKING:
    from ..specifier import StageSpecifier

def instantiate_stage_as_pipeline(
        specifier: Type['StageSpecifier'],
        component_types: Tuple[Type[Component], ...],
        options: OptionsList
) -> Pipeline:
    """
    TODO: Update.

    Creates an instance of the stage represented by this plugin
    as a pipeline, using the given command-line options.

    :param specifier:   The stage specifier to instantiate.
    :param options:     The command-line options.
    :return:            The stage as a pipeline.
    """
    # Instantiate all of the stage's components from the options
    try:
        namespace = get_configured_stage_parser(component_types, prog=specifier.name()).parse_args(options)
    except SystemExit as e:
        raise Exception(f"Error parsing stage options: {e}") from e
    components = tuple(component_type(namespace) for component_type in component_types)

    source = None
    sink = None

    if isinstance(components[0], SourceComponent):
        source = components[0]
        components = components[1:]

    elif isinstance(components[-1], SinkComponent):
        sink = components[-1]
        components = components[:-1]

    return Pipeline(
        source=source,
        processors=components,
        sink=sink
    )
