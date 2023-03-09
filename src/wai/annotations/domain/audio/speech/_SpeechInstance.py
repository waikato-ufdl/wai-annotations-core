from typing import Type

from ....core.domain.specifier import DomainSpecifier
from .._AudioInstance import AudioInstance
from ._Transcription import Transcription


class SpeechInstance(AudioInstance[Transcription]):
    """
    An instance in the speech domain.
    """
    @classmethod
    def domain_specifier(cls: Type['SpeechInstance']) -> Type['DomainSpecifier[SpeechInstance]']:
        from ._SpeechDomainSpecifier import SpeechDomainSpecifier
        return SpeechDomainSpecifier

    @classmethod
    def annotation_type(cls) -> Type[Transcription]:
        return Transcription
