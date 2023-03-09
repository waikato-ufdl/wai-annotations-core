from argparse import ArgumentDefaultsHelpFormatter


class MainUsageFormatter(ArgumentDefaultsHelpFormatter):
    """
    Helper class for formatting the main usage message.
    """
    def _format_usage(self, *args, **kwargs):
        # Get the normal formatting, minus the trailing double-newlines
        super_formatted = super()._format_usage(*args, **kwargs)[:-2]

        return f"{super_formatted} [STAGE [STAGE ...]]\n\n"
