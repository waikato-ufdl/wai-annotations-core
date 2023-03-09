from typing import Iterable, Iterator, Set, TypeVar

T = TypeVar('T')


def unique(
        iterable: Iterable[T]
) -> Iterator[T]:
    """
    Creates an iterator over the unique elements of an iterable.

    :param iterable:
                The iterable to return unique values from.
    :return:
                An iterator over the unique elements of iterable.
    """
    # Keep track of which elements have already been seen
    seen: Set[T] = set()

    for element in iterable:
        # Skip elements we've already seen
        if element in seen:
            continue

        seen.add(element)

        yield element
