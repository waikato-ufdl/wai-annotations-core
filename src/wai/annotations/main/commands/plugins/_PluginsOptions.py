from argparse import ArgumentParser
from dataclasses import fields

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import FlagOption, TypedOption

from ....core.plugin import get_all_plugin_names, AllPluginsByType

ONLY_TYPES_CHOICES = tuple(field.name for field in fields(AllPluginsByType))


class PluginsOptions(CLIInstantiable):
    """
    The options for the 'plugins' command.
    """
    ONLY = TypedOption(
        "-o", "--only",
        type=str,
        nargs="+",
        choices=get_all_plugin_names(),
        help="restrict the set of plugins to only those specified",
        metavar="PLUGIN"
    )

    ONLY_TYPES = TypedOption(
        "-O", "--only-types",
        type=str,
        nargs="+",
        choices=ONLY_TYPES_CHOICES,
        help=f"restricts the set of plugins to only the specified types ({', '.join(ONLY_TYPES_CHOICES)})",
        metavar="TYPE"
    )

    GROUP_BY_TYPE = FlagOption(
        "-g", "--group-by-type",
        help="whether to group the plugins by their function"
    )

    DESCRIPTIONS = FlagOption(
        "-d", "--no-descriptions",
        invert=True,
        help="whether to suppress the descriptions of the plugins"
    )

    DOMAINS = FlagOption(
        "-D", "--no-domains",
        invert=True,
        help="whether to suppress the domains of the plugins"
    )

    OPTIONS = FlagOption(
        "-n", "--no-options",
        invert=True,
        help="whether to suppress the options to the plugin"
    )

    FORMATTING = TypedOption(
        "-f", "--formatting",
        type=str,
        choices=("cli", "markdown"),
        default="cli",
        help="the formatting style to print the plugins in"
    )

    # Override the default help option
    HELP = FlagOption(
        "-h", "--help",
        help="prints this help message and exits"
    )

    @classmethod
    def get_configured_parser(cls, *, add_help=False, **kwargs) -> ArgumentParser:
        return super().get_configured_parser(add_help=add_help, **kwargs)
