from dataclasses import asdict, fields
from typing import Type

from wai.common.cli import OptionsList

from ....core.help import format_stage_usage
from ....core.plugin import get_all_plugins_by_type, AllPluginsByType
from ....core.plugin.specifier import PluginSpecifier
from ....core.stage.specifier import ProcessorStageSpecifier, SourceStageSpecifier, SinkStageSpecifier
from ...logging import get_app_logger
from ._help import plugins_help
from ._PluginsOptions import PluginsOptions

def plugins_main(options: OptionsList):
    """
    Main method which handles the 'plugins' sub-command. Prints the plugins
    registered with wai.annotations.

    :param options:
                The options to the sub-command.
    """
    # Parse the options
    try:
        plugins_options = PluginsOptions(options)
    except ValueError:
        get_app_logger().exception("Couldn't parse options to 'plugins' command")
        print(plugins_help())
        raise

    print(get_plugins_formatted(plugins_options))


def get_plugins_formatted(options: PluginsOptions) -> str:
    """
    Gets a formatted string containing information about the plugins
    registered with wai.annotations, formatted according to the
    provided options.

    :param options:
                The formatting options.
    :return:
                The formatted string.
    """
    # If the help option is selected, print the usage and quit
    if options.HELP:
        print(plugins_help())
        exit()

    # Get the plugins registered with wai.annotations
    plugins = get_all_plugins_by_type()

    # Filter to the specified types
    if len(options.ONLY_TYPES) > 0:
        to_remove = [field.name for field in fields(plugins) if field.name not in options.ONLY_TYPES]
        for plugin_type in to_remove:
            plugin_dict: dict = getattr(plugins, plugin_type)
            plugin_dict.clear()

    # Filter to the specified plugins/types
    if len(options.ONLY) > 0:
        only = set(options.ONLY)
        for plugin_dict in asdict(plugins).values():
            to_remove = [key for key in plugin_dict.keys() if key not in only]
            for key in to_remove:
                plugin_dict.pop(key)

    return (
        format_plugins_by_type(plugins, options)
        if options.GROUP_BY_TYPE else
        format_plugins_no_group_by_type(plugins, options)
    )


def format_plugins_by_type(
        plugins: AllPluginsByType,
        options: PluginsOptions
) -> str:
    """
    Formats the plugins when the group-by-type option is selected.

    :param plugins:
                The plugins, grouped by type.
    :param options:
                The formatting options.
    :return:
                The formatted string.
    """
    # Check if we are doing CLI or Markdown formatting
    cli_formatting = options.FORMATTING == "cli"

    # Header
    result = (
        "PLUGINS:\n"
        if cli_formatting else
        "# Plugins\n"
    )

    # Choose a formatter based on the option
    formatter = (
        format_plugin_cli
        if cli_formatting else
        format_plugin_markdown
    )

    for plugin_type, plugins_for_type in asdict(plugins).items():
        # Skip empty plugin-types
        if len(plugins_for_type) == 0:
            continue

        # Add a heading for the type
        result += (
            f"  {plugin_type.upper()}:\n"
            if cli_formatting else
            f"## {plugin_type.capitalize()}\n"
        )

        # Sort the plugins by name
        names_sorted = list(map(str, plugins_for_type.keys()))
        names_sorted.sort()

        # Format each plugin
        for name in names_sorted:
            result += formatter(name, plugins_for_type[name], options, 3)

        # Additional separation between categories of plugins
        result += "\n"

    return result


def format_plugins_no_group_by_type(
        plugins: AllPluginsByType,
        options: PluginsOptions
) -> str:
    """
    Formats the plugins when not grouped by type.

    :param plugins:
                The plugins to format.
    :param options:
                The formatting options.
    :return:
                The formatted plugins.
    """
    # See if we're doing CLI or Markdown formatting
    cli_formatting = options.FORMATTING == "cli"

    # Header
    result = (
        "PLUGINS:\n"
        if cli_formatting else
        "# Plugins\n"
    )

    # Choose a formatter based on the selected style
    formatter = (
        format_plugin_cli
        if cli_formatting else
        format_plugin_markdown
    )

    # Sort the plugins by name
    names_sorted = list(plugins_for_type.keys() for plugins_for_type in asdict(plugins).values())
    names_sorted.sort()

    # Show 'none' if there are no matched plugins
    if len(names_sorted) == 0:
        result += (
            "  NONE\n"
            if cli_formatting else
            "\nNone\n"
        )

    # Format the plugins
    for name in names_sorted:
        result += formatter(name, plugins[name], options, 4)

    return result


def format_plugin_cli(
        plugin_name: str,
        plugin: Type[PluginSpecifier],
        options: PluginsOptions,
        indent: int
):
    """
    Formats a plugin for the command-line.

    :param plugin_name:
                The name of the plugin.
    :param plugin:
                The plugin specifier.
    :param options:
                The formatting options.
    :param indent:
                The level of indentation.
    :return:
                The formatted plugin.
    """
    # Format the indentation string
    indentation = "  " * indent

    # Add the name
    formatted = f"{indentation}{plugin_name.upper()}"

    # Add a : if there are any other descriptions of the plugin
    if options.DESCRIPTIONS or options.DOMAINS or options.OPTIONS:
        formatted += ":"
    formatted += "\n"

    # Add the description if not suppressed
    if options.DESCRIPTIONS:
        formatted += f"{indentation}  {plugin.description()}\n\n"

    # Add the domains if not suppressed
    # FIXME: Show generic bounds instead of specific domains.
    if options.DOMAINS:
        bound = (
            plugin.bound_relationship() if issubclass(plugin, ProcessorStageSpecifier)
            else plugin.bound() if issubclass(plugin, (SourceStageSpecifier, SinkStageSpecifier))
            else None
        )

        # TODO: Remove try/except once InstanceTypeBoundRelationship __str__ is fully implemented
        try:
            bound = str(bound) if bound is not None else None
        except NotImplementedError:
            bound = "[formatting bound failed]"

        if bound is not None:
            formatted += f"{indentation}  Bound: {bound}\n\n"


    # Add the options if not suppressed
    # TODO: Reinstate once multi-domain components can be joined
    #if options.OPTIONS:
    #    formatted += f"{format_stage_usage(plugin, plugin_name, indent + 2)}\n"

    return formatted


def format_plugin_markdown(
        plugin_name: str,
        plugin: Type[PluginSpecifier],
        options: PluginsOptions,
        indent: int
):
    """
    Formats a plugin in Markdown style.

    :param plugin_name:
                The name of the plugin.
    :param plugin:
                The plugin specifier.
    :param options:
                The formatting options.
    :param indent:
                The level of indentation.
    :return:
                The formatted plugin.
    """
    # Format the indentation string
    indentation = "#" * indent

    # Format the plugin name
    formatted = f"{indentation} {plugin_name.upper()}\n"

    # Add the description if not suppressed
    if options.DESCRIPTIONS:
        formatted += f"{plugin.description()}\n\n"

    # Add the domains if not suppressed
    # FIXME: Show generic bounds instead of specific domains.


    if options.DOMAINS:

        bound = (
            plugin.bound_relationship() if issubclass(plugin, ProcessorStageSpecifier)
            else plugin.bound() if issubclass(plugin, (SourceStageSpecifier, SinkStageSpecifier))
            else None
        )

        # TODO: Remove try/except once InstanceTypeBoundRelationship __str__ is fully implemented
        try:
            bound = str(bound) if bound is not None else None
        except NotImplementedError:
            bound = "[formatting bound failed]"

        if bound is not None:
            formatted += f"{indentation}# Bound:\n{bound}\n\n"

    # Add the options if not suppressed
    # TODO: Reinstate once multi-domain components can be joined
    #if options.OPTIONS:
    #    formatted += f"{indentation}# Options:\n```\n{format_stage_usage(plugin, plugin_name, 0)}```\n\n"

    return formatted
