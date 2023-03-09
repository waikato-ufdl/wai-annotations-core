from typing import Any, Tuple, Union


def is_subtype(
        value: Any,
        types: Union[type, Tuple[type, ...]]
) -> bool:
    """
    Checks if the given value is a type that is a sub-type of any of the
    given types.

    :param value:
                The value to check.
    :param types:
                The types to check for sub-typing.
    :return:
                Whether the value is a sub-type of any of the given types.
    """
    return (
        isinstance(value, type)
        and issubclass(value, types)
    )
