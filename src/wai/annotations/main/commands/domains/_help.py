"""
Provides the help information for the 'domains' sub-command.
"""
from ....core.help import MainUsageFormatter
from ._DomainsOptions import DomainsOptions


def domains_help() -> str:
    """
    Gets the help text for the 'domains' sub-command.
    """
    return DomainsOptions.get_configured_parser(
        prog="wai-annotations domains",
        formatter_class=MainUsageFormatter).format_help()
