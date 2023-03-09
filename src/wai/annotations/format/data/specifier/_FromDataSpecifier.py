from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import Annotation, Data, Instance
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundUnion
from ....core.stage.specifier import SourceStageSpecifier


class FromDataSpecifier(
    SourceStageSpecifier[DomainSpecifier[Instance[Data, Annotation]]]
):
    """
    Specifier for the from-data source.
    """
    @classmethod
    def name(cls) -> str:
        return "From Data"

    @classmethod
    def description(cls) -> str:
        return "Produces unannotated instances from data-files."

    @classmethod
    def bound(cls) -> InstanceTypeBoundUnion:
        return InstanceTypeBoundUnion.any()

    @classmethod
    def components(
            cls,
            domain: Type[DomainSpecifier[Instance[Data, Annotation]]]
    ) -> Tuple[Type[Component], ...]:
        from ....core.component.util.input import ReadableStoreSource

        # Import the base FromData component
        from ..component import FromData

        # Specialise it for the selected source domain
        class DomainSpecialisedFromData(
            FromData[
                Tuple['StoreKey', bytes, 'ReadableStore', bool],  # FIXME: Bug: Python doesn't recognise that this generic parameter
                                                                  #             is already set in FileDataProcessor.
                Instance[Data, Annotation]
            ]):
            @classmethod
            def instance_type(cls) -> Type[Instance[Data, Annotation]]:
                return domain.instance_type()

        return ReadableStoreSource, DomainSpecialisedFromData
