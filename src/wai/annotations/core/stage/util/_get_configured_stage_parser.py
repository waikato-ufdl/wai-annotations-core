from argparse import ArgumentParser
from typing import Tuple, Type

from ...component import Component


def get_configured_stage_parser(
        component_types: Tuple[Type[Component], ...],
        **kwargs
) -> ArgumentParser:
    """
    TODO: Update.

    Gets a parser which is configured to parse the options
    for all components of the given stage specifier.

    :param specifier:   The specifier to create the parser for.
    :param kwargs:      Any additional arguments to the parser.
    :return:            The configured parser for the stage.
    """
    # Force suppression of help option
    kwargs['add_help'] = False

    # Configure a parser on the first component
    parser = component_types[0].get_configured_parser(**kwargs)

    # Update the parser with the remaining components
    for component_type in component_types[1:]:
        component_type.configure_parser(parser)

    return parser
