"""
Provides the help information for the 'batch-split' sub-command.
"""
from ....core.help import MainUsageFormatter
from ._BatchSplitOptions import BatchSplitOptions


def batch_split_help() -> str:
    """
    Gets the help text for the 'batch-split' sub-command.
    """
    return BatchSplitOptions.get_configured_parser(
        prog="wai-annotations batch-split",
        formatter_class=MainUsageFormatter).format_help()
