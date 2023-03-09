from typing import Any, Dict, Tuple, Type, TypeVar

from .._PluginSpecifier import PluginSpecifier
from ._validate_class_method import validate_class_method

ExpectedType = TypeVar('ExpectedType', bound=PluginSpecifier)


def validate_plugin_specifier(
        specifier: Any,
        expected_type: Type[ExpectedType],
        **class_methods: type
) -> Tuple[Type[ExpectedType], Dict[str, Any]]:
    """
    Checks that the given plugin-specifier implements the expected protocol correctly.
    """
    if not isinstance(specifier, type):
        raise TypeError(f"Expected type, received {type(specifier).__qualname__}")
    if not issubclass(specifier, expected_type):
        raise TypeError(f"Expected sub-class of {expected_type.__qualname__}, received {specifier.__qualname__}")

    # Add the name and description class-methods from the PluginSpecifier base-class
    class_methods.update(
        {
            PluginSpecifier.name.__name__: str,
            PluginSpecifier.description.__name__: str
        }
    )

    # Validate all class methods
    class_method_return_values: Dict[str, Any] = {
        class_method: validate_class_method(specifier, class_method, expected_return_type)
        for class_method, expected_return_type in class_methods.items()
    }

    return specifier, class_method_return_values
