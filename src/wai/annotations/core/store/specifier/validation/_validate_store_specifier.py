from typing import Any, Type

from ....plugin.specifier.validation import validate_plugin_specifier
from ..._Store import Store
from .._StoreSpecifier import StoreSpecifier


def validate_store_specifier(
        specifier: Any
) -> Type[StoreSpecifier]:
    """
    Validates a store specifier.
    """
    store_specifier, class_method_return_values = validate_plugin_specifier(
        specifier,
        StoreSpecifier,
        **{
            StoreSpecifier.store_type.__name__: type
        }
    )

    # Store-type must not only be a type, but a sub-class of Store
    store_type = class_method_return_values[StoreSpecifier.store_type.__name__]
    if not issubclass(store_type, Store):
        raise ValueError(
            f"Expected class-method '{StoreSpecifier.store_type.__name__}' "
            f"to return a sub-class of {Store.__qualname__}, received {store_type.__qualname__}"
        )

    # Store should be either readable or writable to be useful
    if not store_specifier.is_readable() and not store_specifier.is_writable():
        raise ValueError(
            f"Store-type {store_type.__qualname__} is neither readable nor writable"
        )

    return store_specifier
