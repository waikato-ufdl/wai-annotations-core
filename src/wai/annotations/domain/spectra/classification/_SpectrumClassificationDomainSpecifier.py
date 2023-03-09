from typing import Type

from ....core.domain.specifier import DomainSpecifier
from ._SpectrumClassificationInstance import SpectrumClassificationInstance

DESCRIPTION = """Spectra categorised by target.

The spectrum classification domain deals with labelling spectra as identifying a certain substance. Instances in this
domain contain a spectrum and a string label classifying the spectrum.
"""


class SpectrumClassificationDomainSpecifier(DomainSpecifier[SpectrumClassificationInstance]):
    """
    Domain specifier for spectra annotated with a label
    classifying the contents of the spectrum.
    """
    @classmethod
    def name(cls) -> str:
        return "Spectrum Classification Domain"

    @classmethod
    def description(cls) -> str:
        return DESCRIPTION

    @classmethod
    def instance_type(cls) -> Type[SpectrumClassificationInstance]:
        return SpectrumClassificationInstance
