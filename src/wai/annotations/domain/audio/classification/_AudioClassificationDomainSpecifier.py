from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ._AudioClassificationInstance import AudioClassificationInstance

DESCRIPTION = """Transcriptions of recorded speech.

The speech domain covers audio data of people speaking natural languages, annotated with text transcribing the verbal
contents of the audio. Instances in this domain are an audio file and a string containing the transcription.
"""


class AudioClassificationDomainSpecifier(DomainSpecifier[AudioClassificationInstance]):
    """
    Domain specifier for audio recordings annotated with a label.
    """
    @classmethod
    def name(cls) -> str:
        return "Audio classification domain"
    
    @classmethod
    def description(cls) -> str:
        return DESCRIPTION

    @classmethod
    def instance_type(cls) -> Type[AudioClassificationInstance]:
        return AudioClassificationInstance
