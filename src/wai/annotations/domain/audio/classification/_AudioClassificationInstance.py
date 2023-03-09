from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ...classification import Classification
from .._AudioInstance import AudioInstance


class AudioClassificationInstance(AudioInstance[Classification]):
    """
    An instance in the audio classification domain.
    """
    @classmethod
    def domain_specifier(cls: Type['AudioClassificationInstance']) -> Type['DomainSpecifier[AudioClassificationInstance]']:
        from ._AudioClassificationDomainSpecifier import AudioClassificationDomainSpecifier
        return AudioClassificationDomainSpecifier

    @classmethod
    def annotation_type(cls) -> Type[Classification]:
        return Classification
