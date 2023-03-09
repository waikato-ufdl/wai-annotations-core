from typing import Callable, List, TypeVar

T = TypeVar('T')


def reduce_subsumes(
        subsumes: Callable[[T, T], bool],
        *items: T
) -> List[T]:
    """
    Reduces a set of items to only those that aren't subsumed by any other item.

    :param subsumes:
                Function which determines if its first input is subsumed by its second.
    :param items:
                The items to reduce.
    :return:
                A list of items that aren't subsumed by other items.
    """
    # No items, no result
    if len(items) == 0:
        return []

    reduced_items: List[T] = [items[0]]

    for item in items[1:]:
        # If any of the already reduced items subsumes this item, ignore it
        if any(subsumes(item, reduced_item) for reduced_item in reduced_items):
            continue

        # Find out which items this item subsumes
        indices_of_subsumed_reduced_items = [
            index
            for index, reduced_item in enumerate(reduced_items)
            if subsumes(reduced_item, item)
        ]

        # Remove them from the set of reduced items
        for index in reversed(indices_of_subsumed_reduced_items):
            reduced_items.pop(index)

        # Add this item to the reduced set
        reduced_items.append(item)

    return reduced_items
