class BadPluginName(Exception):
    """
    Error for when a plugin-name is invalid.
    """
    def __init__(self, name: str, reason: str):
        super().__init__(
            f"Bad plugin name '{name}': {reason}"
        )
