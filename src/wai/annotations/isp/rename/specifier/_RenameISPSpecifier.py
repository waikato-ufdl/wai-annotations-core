from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain.specifier import DomainSpecifier
from ....core.stage.bounds import InstanceTypeBoundRelationship, InstanceTypeBoundUnion
from ....core.stage.specifier import ProcessorStageSpecifier


class RenameISPSpecifier(ProcessorStageSpecifier):
    """
    ISP that renames files.
    """
    @classmethod
    def name(cls) -> str:
        return "Rename ISP"

    @classmethod
    def description(cls) -> str:
        return "ISP that renames files."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        # works in any domain
        return input_domain

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            InstanceTypeBoundUnion.any(),
            InstanceTypeBoundUnion.any(),
            input_instance_type_must_match_output_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...rename.component import Rename
        return Rename,
