from typing import Type, TypeVar, TYPE_CHECKING

from ....core.domain import Instance
from ....core.domain.specifier import DomainSpecifier
from ...classification import Classification
from .._Spectrum import Spectrum


SelfType = TypeVar('SelfType', bound='SpectrumClassificationInstance')


class SpectrumClassificationInstance(Instance[Spectrum, Classification]):
    """
    An item in a spectrum-classification data-set.
    """
    @classmethod
    def domain_specifier(cls: Type[SelfType]) -> Type['DomainSpecifier[SelfType]']:
        from ._SpectrumClassificationDomainSpecifier import SpectrumClassificationDomainSpecifier
        return SpectrumClassificationDomainSpecifier

    @classmethod
    def data_type(cls) -> Type[Spectrum]:
        return Spectrum

    @classmethod
    def annotation_type(cls) -> Type[Classification]:
        return Classification
