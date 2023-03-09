from typing import Any, Type

from ....plugin.specifier.validation import validate_plugin_specifier
from ..._Instance import Instance
from .._DomainSpecifier import DomainSpecifier


def validate_domain_specifier(
        specifier: Any
) -> Type[DomainSpecifier]:
    """
    Validates a domain specifier.
    """
    domain_specifier, class_method_return_values = validate_plugin_specifier(
        specifier,
        DomainSpecifier,
        **{
            DomainSpecifier.instance_type.__name__: type
        }
    )

    # Instance-type must not only be a type, but a sub-class of Instance
    instance_type = class_method_return_values[DomainSpecifier.instance_type.__name__]
    if not issubclass(instance_type, Instance):
        raise ValueError(
            f"Expected class-method '{DomainSpecifier.instance_type.__name__}' "
            f"to return a sub-class of {Instance.__qualname__}, received {instance_type.__qualname__}"
        )

    return domain_specifier
