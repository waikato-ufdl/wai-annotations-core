from typing import NoReturn, Any


def raise_expression(
        exception: Any
) -> NoReturn:
    """
    Allows for the use of raise as an expression.

    :param exception:
                The exception to raise.
    :raises Any:
                The given exception.
    """
    raise exception
