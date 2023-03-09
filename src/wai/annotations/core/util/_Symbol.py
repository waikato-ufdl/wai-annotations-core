from typing import Any


class Symbol:
    """
    Object representing a unique value.
    """
    def __init__(
            self,
            description: str = ""
    ):
        """
        :param description:
                    A description of the symbol for debugging purposes.
        """
        self._description = description
    def __repr__(self):
        return f"Symbol({self._description})"

    def __eq__(self, other: Any) -> bool:
        return other is self

    def __hash__(self):
        return hash(id(self))
