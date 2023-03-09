from typing import Type

from ..stage.specifier import StageSpecifier, ProcessorStageSpecifier
from ..stage.util import get_configured_stage_parser
from ._plugin_usage_formatter_with_default_start_indent import plugin_usage_formatter_with_default_start_indent


def format_stage_usage(
        specifier: Type[StageSpecifier],
        name: str,
        indent: int = 0
) -> str:
    """
    Formats the usage text for a plugin stage.

    :param specifier:   The stage specifier
    :param name:        The name the plugin is registered under in the plugin system.
    :param indent:      The indentation level of the text.
    :return:            The usage text.
    """
    # FIXME: How to format the usage of components which may have different options depending on the
    #        domain they are being used in?
    raise NotImplementedError(format_stage_usage.__qualname__)

    components = (
        specifier.components(specifier.bound_relationship()) if issubclass(specifier, ProcessorStageSpecifier)
        else specifier.components()
    )
    return (" " * indent) + get_configured_stage_parser(
        specifier,
        prog=name,
        formatter_class=plugin_usage_formatter_with_default_start_indent(indent)
    ).format_help()
