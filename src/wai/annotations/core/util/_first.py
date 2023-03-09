from typing import Callable, Iterable, TypeVar, Union

from ._Symbol import Symbol


# The type of elements of the iterable.
T = TypeVar('T')
# The type of the default value.
Default = TypeVar('Default')


def first(
        iterable: Iterable[T],
        predicate: Callable[[T], bool],
        default: Default
) -> Union[T, Default]:
    """
    Returns the first value from an iterable which meets some predicate. If no
    predicated value is found, returns a default value.

    :param iterable:
                The iterable to search.
    :param predicate:
                The predicate to search for.
    :param default:
                The default value to return if no value matches the predicate.
    :return:
                The first found value matching the predicate,
                or default if none is found.
    """
    for value in iterable:
        if predicate(value):
            return value

    return default


def first_lazy_default(
        iterable: Iterable[T],
        predicate: Callable[[T], bool],
        default: Callable[[], Default]
) -> Union[T, Default]:
    """
    Returns the first value from an iterable which meets some predicate. If no
    predicated value is found, calculates a default value.

    :param iterable:
                The iterable to search.
    :param predicate:
                The predicate to search for.
    :param default:
                Callable which calculates the default value to return if no
                value matches the predicate.
    :return:
                The first found value matching the predicate,
                or the calculated default if none is found.
    """
    # Create a unique symbol to indicate that first didn't find anything
    default_symbol = Symbol("First found no predicated item")

    # Defer to first to see if a predicated value is found
    result = first(iterable, predicate, default_symbol)

    # If so, return it
    if result is not default_symbol:
        return result

    # If not, lazily calculate and return the default
    return default()
