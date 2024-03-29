from typing import Type

from ....core.domain import DomainSpecifier

from ._VoidOutputFormatSpecifier import VoidOutputFormatSpecifier


class VoidSPOutputFormatSpecifier(VoidOutputFormatSpecifier):
    """
    Specifier for the void-writer in the speech domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Consumes speech instances without writing them."

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
