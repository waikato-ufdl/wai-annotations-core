from typing import TypeVar, Type

from .._PluginSpecifier import PluginSpecifier

ExpectedType = TypeVar('ExpectedType')


def validate_class_method(
        specifier: Type[PluginSpecifier],
        method: str,
        expected_type: Type[ExpectedType]
) -> ExpectedType:
    """
    Validates a single class-method of a plugin-specifier.
    """
    # Get the class method
    class_method = getattr(specifier, method, None)

    if class_method is None:
        raise ValueError(f"Expected class-method '{method}' not found")

    if not callable(class_method):
        raise ValueError(f"Expected class-method '{method}' to be callable")

    try:
        # Call the class-method
        # TODO: Check if class is required to be passed manually e.g. class_method(specifier)
        value = class_method()
    except Exception as e:
        raise ValueError(f"Class-method '{method}' raised: {e}") from e

    if not isinstance(value, expected_type):
        raise ValueError(
            f"Class-method '{method}' returned a {type(value).__qualname__} "
            f"when a {expected_type.__qualname__} was expected"
        )

    return value
