from typing import Tuple, Type

from ....core.component import ProcessorComponent
from ....core.domain import Data, Instance
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.classification import Classification
from ....domain.image.object_detection import DetectedObjects


class OD2ICXDCSpecifier(ProcessorStageSpecifier):
    """
    Specifies the image object-detection -> image classification
    cross-domain converter.
    """

    @classmethod
    def name(cls) -> str:
        return "OD -> IC"

    @classmethod
    def description(cls) -> str:
        return "Converts image object-detection instances into image classification instances"

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            (Data, DetectedObjects),
            (Data, Classification),
            input_data_type_must_match_output_data_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ..component import OD2ICXDC

        output_type = bound_relationship.output_bound.as_single
        if output_type is None:
            raise Exception(
                f"Output-bound {bound_relationship.output_bound} is to general, must be a specific instance type"
            )

        class OutputSpecificOD2ICXDC(OD2ICXDC[output_type]):
            @classmethod
            def output_type(cls) -> 'output_type':
                return output_type

        return OutputSpecificOD2ICXDC,
