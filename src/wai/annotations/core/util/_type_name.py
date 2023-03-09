from typing import Any


def type_name(value: Any) -> str:
    """
    Gets the type-name of the value's type, or of the value itself
    if it is a type.

    :param value:
                The value or type to get the name of.
    :return:
                The name.
    """
    if isinstance(value, type):
        return value.__qualname__
    else:
        return type(value).__qualname__
