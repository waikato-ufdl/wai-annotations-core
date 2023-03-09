from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Annotation, Data
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier


class CheckDuplicateKeysISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the duplicate-keys checker.
    """
    @classmethod
    def name(cls) -> str:
        return "Check Duplicate Keys"

    @classmethod
    def description(cls) -> str:
        return (
            "Causes the conversion stream to halt when multiple dataset items "
            "have the same key"
        )

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            (Data, Annotation),
            (Data, Annotation),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ..component import CheckDuplicateKeys
        return CheckDuplicateKeys,
