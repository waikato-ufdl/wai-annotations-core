from typing import Any


def describe_value(
        value: Any
) -> str:
    """
    Describes a value.

    :param value:
                The value to describe.
    :return:
                The description.
    """
    if isinstance(value, type):
        return f"class '{value.__qualname__}'"
    else:
        return f"instance of '{type(value).__qualname__}'"
