from typing import Optional, Tuple, Type, Union, TYPE_CHECKING

from ...domain import Annotation, Data
from ._InstanceTypeBound import InstanceTypeBound, RawInstanceTypeBound
from ._InstanceTypeBoundUnion import InstanceTypeBoundUnion

if TYPE_CHECKING:
    from ...domain.specifier import DomainSpecifier

class InstanceTypeBoundRelationship:
    """
    Represents the relationship between the input and output instance type-bounds
    for a processor stage.
    """
    def __init__(
            self,
            input_bound: Union[InstanceTypeBoundUnion, InstanceTypeBound, RawInstanceTypeBound],
            output_bound: Union[InstanceTypeBoundUnion, InstanceTypeBound, RawInstanceTypeBound],
            *,
            input_data_type_must_match_output_data_type: bool = False,
            input_annotation_type_must_match_output_annotation_type: bool = False,
            input_instance_type_must_match_output_instance_type: bool = False,
            output_data_type_must_match_input_data_type: bool = False,
            output_annotation_type_must_match_input_annotation_type: bool = False,
            output_instance_type_must_match_input_instance_type: bool = False
    ):
        if not isinstance(input_bound, InstanceTypeBoundUnion):
            input_bound = InstanceTypeBoundUnion(input_bound)
        if not isinstance(output_bound, InstanceTypeBoundUnion):
            output_bound = InstanceTypeBoundUnion(output_bound)

        self._input_bound, self._output_bound = self._check_init_args(
            input_bound,
            output_bound,
            input_data_type_must_match_output_data_type,
            input_annotation_type_must_match_output_annotation_type,
            input_instance_type_must_match_output_instance_type,
            output_data_type_must_match_input_data_type,
            output_annotation_type_must_match_input_annotation_type,
            output_instance_type_must_match_input_instance_type
        )
        self._input_data_type_must_match_output_data_type = input_data_type_must_match_output_data_type
        self._input_annotation_type_must_match_output_annotation_type = input_annotation_type_must_match_output_annotation_type
        self._input_instance_type_must_match_output_instance_type = input_instance_type_must_match_output_instance_type
        self._output_data_type_must_match_input_data_type = output_data_type_must_match_input_data_type
        self._output_annotation_type_must_match_input_annotation_type = output_annotation_type_must_match_input_annotation_type
        self._output_instance_type_must_match_input_instance_type = output_instance_type_must_match_input_instance_type

    def intersect_input_bound(self, other: InstanceTypeBoundUnion) -> Optional['InstanceTypeBoundRelationship']:
        intersected_input_bound = self._input_bound.intersection_bound(other)
        if intersected_input_bound is None:
            return None

        try:
            return InstanceTypeBoundRelationship(
                intersected_input_bound,
                self._output_bound,
                input_data_type_must_match_output_data_type=self._input_data_type_must_match_output_data_type,
                input_annotation_type_must_match_output_annotation_type=self._input_annotation_type_must_match_output_annotation_type,
                input_instance_type_must_match_output_instance_type=self._input_instance_type_must_match_output_instance_type,
                output_data_type_must_match_input_data_type=self._output_data_type_must_match_input_data_type,
                output_annotation_type_must_match_input_annotation_type=self._output_annotation_type_must_match_input_annotation_type,
                output_instance_type_must_match_input_instance_type=self._output_instance_type_must_match_input_instance_type,
            )
        except ValueError:
            return None

    def for_input_domain(self, domain: Type['DomainSpecifier']) -> Optional['InstanceTypeBoundRelationship']:
        return self.intersect_input_bound(InstanceTypeBoundUnion.for_domain(domain))

    def intersect_output_bound(self, other: InstanceTypeBoundUnion) -> Optional['InstanceTypeBoundRelationship']:
        intersected_output_bound = self._output_bound.intersection_bound(other)
        if intersected_output_bound is None:
            return None

        try:
            return InstanceTypeBoundRelationship(
                self._input_bound,
                intersected_output_bound,
                input_data_type_must_match_output_data_type=self._input_data_type_must_match_output_data_type,
                input_annotation_type_must_match_output_annotation_type=self._input_annotation_type_must_match_output_annotation_type,
                input_instance_type_must_match_output_instance_type=self._input_instance_type_must_match_output_instance_type,
                output_data_type_must_match_input_data_type=self._output_data_type_must_match_input_data_type,
                output_annotation_type_must_match_input_annotation_type=self._output_annotation_type_must_match_input_annotation_type,
                output_instance_type_must_match_input_instance_type=self._output_instance_type_must_match_input_instance_type,
            )
        except ValueError:
            return None

    def for_output_domain(self, domain: Type['DomainSpecifier']) -> Optional['InstanceTypeBoundRelationship']:
        return self.intersect_output_bound(InstanceTypeBoundUnion.for_domain(domain))

    @property
    def input_bound(self):
        return self._input_bound

    @property
    def output_bound(self):
        return self._output_bound

    @property
    def input_data_type_must_match_output_data_type(self) -> bool:
        return self._input_data_type_must_match_output_data_type

    @property
    def input_annotation_type_must_match_output_annotation_type(self) -> bool:
        return self._input_annotation_type_must_match_output_annotation_type

    @property
    def input_instance_type_must_match_output_instance_type(self) -> bool:
        return self._input_instance_type_must_match_output_instance_type

    @property
    def output_data_type_must_match_input_data_type(self) -> bool:
        return self._output_data_type_must_match_input_data_type

    @property
    def output_annotation_type_must_match_input_annotation_type(self) -> bool:
        return self._output_annotation_type_must_match_input_annotation_type

    @property
    def output_instance_type_must_match_input_instance_type(self) -> bool:
        return self._output_instance_type_must_match_input_instance_type

    @staticmethod
    def _check_init_args(
            input_bound: InstanceTypeBoundUnion,
            output_bound: InstanceTypeBoundUnion,
            input_data_type_must_match_output_data_type: bool,
            input_annotation_type_must_match_output_annotation_type: bool,
            input_instance_type_must_match_output_instance_type: bool,
            output_data_type_must_match_input_data_type: bool,
            output_annotation_type_must_match_input_annotation_type: bool,
            output_instance_type_must_match_input_instance_type: bool
    ):
        # Check that the required relationships are possible given the input/output bounds
        if input_instance_type_must_match_output_instance_type:
            reduced_input_bound = input_bound.intersection_bound(output_bound)
            if reduced_input_bound is None:
                raise ValueError(
                    f"Input instance type can't match output instance type as there is no "
                    f"overlap between input-bound '{input_bound}' and output-bound '{output_bound}'"
                )
        else:
            reduced_input_bound = InstanceTypeBoundRelationship._check_must_match(
                input_bound,
                "input",
                output_bound,
                "output",
                input_data_type_must_match_output_data_type,
                input_annotation_type_must_match_output_annotation_type
            )

        if output_instance_type_must_match_input_instance_type:
            reduced_output_bound = output_bound.intersection_bound(input_bound)
            if reduced_output_bound is None:
                raise ValueError(
                    f"Output instance type can't match input instance type as there is no "
                    f"overlap between output-bound '{output_bound}' and input-bound '{input_bound}'"
                )
        else:
            reduced_output_bound = InstanceTypeBoundRelationship._check_must_match(
                output_bound,
                "output",
                input_bound,
                "input",
                output_data_type_must_match_input_data_type,
                output_annotation_type_must_match_input_annotation_type
            )

        return reduced_input_bound, reduced_output_bound

    @staticmethod
    def _check_must_match(
            primary_bound: InstanceTypeBoundUnion,
            primary_bound_name: str,
            secondary_bound: InstanceTypeBoundUnion,
            secondary_bound_name: str,
            data_types_must_match: bool,
            annotation_types_must_match: bool,
    ):
        if not data_types_must_match and not annotation_types_must_match:
            return primary_bound

        primary_bound_reductions = (
            [(data_type, Annotation) for data_type in secondary_bound.data_types]
            if not annotation_types_must_match
            else
            [(Data, annotation_type) for annotation_type in secondary_bound.annotation_types]
            if not data_types_must_match
            else
            secondary_bound.as_pairs
        )

        primary_bound_reduction_bound = InstanceTypeBoundUnion(*primary_bound_reductions)

        reduced_primary_bound = primary_bound.intersection_bound(primary_bound_reduction_bound)

        if reduced_primary_bound is None:
            matched_types, examples = (
                ("data", ", ".join(map(str, secondary_bound.data_types)))
                if not annotation_types_must_match
                else
                ("annotation", ", ".join(map(str, secondary_bound.annotation_types)))
                if not data_types_must_match
                else
                ("data/annotation", str(primary_bound_reduction_bound))
            )

            raise ValueError(
                f"{primary_bound_name.capitalize()} {matched_types} type "
                f"can't match "
                f"{secondary_bound_name} {matched_types} type "
                f"as no {secondary_bound_name} {matched_types} type is "
                f"present in {primary_bound_name}-bound {primary_bound}: "
                f"{examples}"
            )

        return reduced_primary_bound

    def __str__(self) -> str:
        def extends(
                ident: str,
                in_bound: str,
                out_bound: str,
                in_extends_out: bool,
                out_extends_in: bool
        ) -> Tuple[str, str, str]:
            if in_extends_out and out_extends_in:
                assert in_bound == out_bound
                return f"{ident} extends {in_bound}", ident, ident
            elif in_extends_out:
                return f"{ident}_in extends {ident}_out, {ident}_out extends {out_bound}", f"{ident}_in", f"{ident}_out"
            elif self._output_instance_type_must_match_input_instance_type:
                return f"{ident}_in extends {in_bound}, {ident}_out extends {ident}_in", f"{ident}_in", f"{ident}_out"
            else:
                return f"{ident}_in extends {in_bound}, {ident}_out extends {out_bound}", f"{ident}_in", f"{ident}_out"

        if (
                self._input_instance_type_must_match_output_instance_type
                or self._output_instance_type_must_match_input_instance_type
        ):
            generics, in_param, out_param = extends(
                "I",
                str(self._input_bound),
                str(self._output_bound),
                self._input_instance_type_must_match_output_instance_type,
                self._output_instance_type_must_match_input_instance_type
            )
        else:
            if self._input_data_type_must_match_output_data_type or self._output_data_type_must_match_input_data_type:
                data_generics, data_in_param, data_out_param = extends(
                    "D",
                    " | ".join(data_type.__name__ for data_type in self._input_bound.data_types),
                    " | ".join(data_type.__name__ for data_type in self._output_bound.data_types),
                    self._input_data_type_must_match_output_data_type,
                    self._output_data_type_must_match_input_data_type
                )
            else:
                data_generics, data_in_param, data_out_param = None, "Data", "Data"

            if self._input_annotation_type_must_match_output_annotation_type or self._output_annotation_type_must_match_input_annotation_type:
                annotation_generics, annotation_in_param, annotation_out_param = extends(
                    "A",
                    " | ".join(annotation_type.__name__ for annotation_type in self._input_bound.annotation_types),
                    " | ".join(annotation_type.__name__ for annotation_type in self._output_bound.annotation_types),
                    self._input_annotation_type_must_match_output_annotation_type,
                    self._output_annotation_type_must_match_input_annotation_type
                )
            else:
                annotation_generics, annotation_in_param, annotation_out_param = None, "Annotation", "Annotation"

            if data_generics is not None or annotation_generics is not None:
                # TODO: Spread intersection across union where it can be reduced for clarity
                instance_in_intersection = f"Instance[{data_in_param}, {annotation_in_param}] & ({self._input_bound})"
                instance_out_intersection = f"Instance[{data_out_param}, {annotation_out_param}] & ({self._output_bound})"
            else:
                instance_in_intersection = str(self._input_bound)
                instance_out_intersection = str(self._output_bound)

            generics, in_param, out_param = extends(
                "I",
                instance_in_intersection,
                instance_out_intersection,
                False,
                False
            )

            if annotation_generics is not None:
                generics = f"{annotation_generics}, {generics}"

            if data_generics is not None:
                generics = f"{data_generics}, {generics}"

        return f"<{generics}>({in_param}) -> {out_param}"
