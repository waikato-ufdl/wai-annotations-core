import itertools
from typing import Dict, Iterable, Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from ....stage.bounds import InstanceTypeBoundUnion
from ....util import raise_expression, describe_value
from ...error import BadPluginSpecifier
from .constants import SOURCE_SINK_DOMAIN_CODE_SUFFIX_MATCHER, PROCESSOR_DOMAIN_CODE_SUFFIX_MATCHER
from ._DomainCode import DomainCode

if TYPE_CHECKING:
    from ....domain.specifier import DomainSpecifier
    from ....stage.specifier import StageSpecifier

SelfType = TypeVar('SelfType')
StageSpecifierType = TypeVar('StageSpecifierType', bound='StageSpecifier')


class DomainSuffix:
    def __init__(
            self,
            suffix: str,
            for_processor: bool
    ):
        matcher = (
            PROCESSOR_DOMAIN_CODE_SUFFIX_MATCHER if for_processor
            else SOURCE_SINK_DOMAIN_CODE_SUFFIX_MATCHER
        )

        match = matcher(suffix)
        if match is None:
            raise Exception(f"Invalid domain suffix '{suffix}'")
        self._suffix = match[1]
        self._for_processor = for_processor

    @classmethod
    def try_parse(
            cls,
            suffix: str,
            for_processor: bool
    ) -> Optional['DomainSuffix']:
        try:
            return DomainSuffix(suffix, for_processor)
        except Exception:
            return None

    def __str__(self) -> str:
        return self._suffix

    @property
    def for_processor(self) -> bool:
        return self._for_processor

    @property
    def source_or_sink(self) -> str:
        if self._for_processor:
            raise Exception("Domain-suffix '{self}' is for a processor")
        return self._suffix

    @property
    def source_or_sink_domain_code(self) -> DomainCode:
        return DomainCode(self.source_or_sink[-2:])

    def source_or_sink_refine_bound(
            self,
            bound: InstanceTypeBoundUnion
    ) -> Optional[InstanceTypeBoundUnion]:
        # FIXME: What is this?
        return

    @property
    def processor(self) -> str:
        if not self._for_processor:
            raise Exception("Domain-suffix '{self}' is for a source or sink")
        return self._suffix

    @property
    def processor_domain_codes(self) -> Tuple[Optional[DomainCode], Optional[DomainCode]]:
        domain_suffix = self.processor
        return (
            (DomainCode(domain_suffix[-5:-3]), DomainCode(domain_suffix[-2:]))
            if len(domain_suffix) == 6  # domain_suffix: -dc-dc
            else (DomainCode(domain_suffix[-2:]), DomainCode(domain_suffix[-2:]))
            if len(domain_suffix) == 3  # domain_suffix: -dc
            else (DomainCode(domain_suffix[-2:]), None)
            if len(domain_suffix) == 8 and domain_suffix.startswith("-from-")  # domain_suffix: -from-dc
            else (None, DomainCode(domain_suffix[-2:]))
            if len(domain_suffix) == 8 and domain_suffix.startswith("-into-")  # domain_suffix: -into-dc
            else raise_expression(
                NotImplementedError(
                    f"PROCESSOR_DOMAIN_CODE_SUFFIX_MATCHER matched unknown domain suffix '{domain_suffix}'"
                )
            )
        )

    def is_valid_for_stage_specifier(
            self,
            stage_specifier: Type['StageSpecifier'],
            domains: Dict[DomainCode, Type['DomainSpecifier']],
            *,
            exact: bool = True
    ) -> Optional[str]:
        """
        Whether this domain-suffix is appropriate for the given type of stage.

        :param stage_specifier:
                    The type of stage that the suffix might be used with.
        :param domains:
                    Domain specifier look-up from domain-codes.
        :param exact:
                    Whether the stage should only allow the domains specified by this suffix,
                    or should at least allow those domains.
        :return:
                    None if the domain-suffix is valid for the stage, or an error reason if not.
        """
        from ....stage.specifier import ProcessorStageSpecifier, SourceStageSpecifier, SinkStageSpecifier

        # The type of stage specifier given (for error reasons)
        stage_type = (
            "Source" if issubclass(stage_specifier, SourceStageSpecifier)
            else "Processor" if issubclass(stage_specifier, ProcessorStageSpecifier)
            else "Sink"
        )

        def unknown_domain_code(domain_code: DomainCode) -> str:
            return (
                f"{stage_type}-stage plugin name contains domain suffix {self} "
                f"which contains unknown domain-code '{domain_code}'"
            )

        def lookup_domain_code(domain_code: Optional[DomainCode]) -> Union[None, str, Type['DomainSpecifier']]:
            domain_specifier: Optional[Type[DomainSpecifier]] = None

            if domain_code is not None:
                domain_specifier = domains.get(domain_code, None)
                if domain_specifier is None:
                    return unknown_domain_code(domain_code)

            return domain_specifier


        if issubclass(stage_specifier, ProcessorStageSpecifier):
            # Get the input and output domains that this suffix implies
            input_domain_code, output_domain_code = self.processor_domain_codes

            # Get the bound-relationship for the stage
            bound_relationship = stage_specifier.bound_relationship()

            # Lookup the input/output domains specified by the suffices
            input_domain_specifier = lookup_domain_code(input_domain_code)
            if isinstance(input_domain_specifier, str):
                return input_domain_specifier
            output_domain_specifier = lookup_domain_code(output_domain_code)
            if isinstance(output_domain_specifier, str):
                return output_domain_specifier

            # Check the input bound is valid for the input domain
            if input_domain_specifier is not None:
                reason = self.validate_bound_for_domain(
                    input_domain_specifier,
                    bound_relationship.input_bound,
                    stage_type,
                    input_domain_code,
                    exact=exact
                )
                if reason is not None:
                    return reason

            # Check the output bound is valid for the output domain
            if output_domain_specifier is not None:
                reason = self.validate_bound_for_domain(
                    output_domain_specifier,
                    bound_relationship.output_bound,
                    stage_type,
                    output_domain_code,
                    exact=exact
                )
                if reason is not None:
                    return reason

            # If both input and output domains are constrained, make sure that the relationship allows those domains
            if input_domain_specifier is not None and output_domain_specifier is not None:
                output_reduced_bound_relationship = bound_relationship.for_output_domain(output_domain_specifier)
                if output_reduced_bound_relationship is None:
                    return (
                        f"{stage_type}-stage plugin name contains domain suffix {self}, "
                        f"which contains output domain-code '{output_domain_code}', "
                        f"which is invalid for the plugin"
                    )
                reason = self.validate_bound_for_domain(
                    input_domain_specifier,
                    output_reduced_bound_relationship.input_bound,
                    stage_type,
                    input_domain_code,
                    exact=exact
                )
                if reason is not None:
                    return reason

                input_reduced_bound_relationship = bound_relationship.for_input_domain(input_domain_specifier)
                if input_reduced_bound_relationship is None:
                    return (
                        f"{stage_type}-stage plugin name contains domain suffix {self}, "
                        f"which contains input domain-code '{output_domain_code}', "
                        f"which is invalid for the plugin"
                    )
                reason = self.validate_bound_for_domain(
                    output_domain_specifier,
                    input_reduced_bound_relationship.output_bound,
                    stage_type,
                    output_domain_code,
                    exact=exact
                )
                if reason is not None:
                    return reason
        elif issubclass(stage_specifier, (SourceStageSpecifier, SinkStageSpecifier)):
            domain_code = self.source_or_sink_domain_code
            domain_specifier = domains.get(domain_code, None)
            if domain_specifier is None:
                return unknown_domain_code(domain_code)
            reason = self.validate_bound_for_domain(
                domain_specifier,
                stage_specifier.bound(),
                stage_type,
                domain_code,
                exact=exact
            )
            if reason is not None:
                return reason
        else:
            raise BadPluginSpecifier(f"Unknown stage specifier '{describe_value(stage_specifier)}'")

        return None

    @staticmethod
    def all_domain_suffices(
            stage_specifier: Type[StageSpecifierType],
            domains: Dict[DomainCode, Type['DomainSpecifier']]
    ) -> Iterable['DomainSuffix']:
        from ....stage.specifier import ProcessorStageSpecifier, SourceStageSpecifier, SinkStageSpecifier

        if issubclass(stage_specifier, ProcessorStageSpecifier):
            return (
                DomainSuffix(suffix_string, True)
                for suffix_string in itertools.chain(
                    (f"-{dc}" for dc in domains),
                    (f"-{dc1}-{dc2}" for dc1 in domains for dc2 in domains),
                    (f"-from-{dc}" for dc in domains),
                    (f"-into-{dc}" for dc in domains)
                )
            )
        elif issubclass(stage_specifier, (SourceStageSpecifier, SinkStageSpecifier)):
            return (
                DomainSuffix(f"-{dc}", False)
                for dc in domains
            )
        else:
            raise BadPluginSpecifier(f"Unknown stage specifier '{describe_value(stage_specifier)}'")

    def validate_bound_for_domain(
            self,
            domain_specifier: Type['DomainSpecifier'],
            bound: InstanceTypeBoundUnion,
            stage_type: str,
            domain_code: DomainCode,
            *,
            exact: bool = True
    ) -> Optional[str]:
        """
        Validates that a stage with a name ending in a domain-suffix has a bound
        matching the instance-type of that domain.

        :param domains:
                    All domains in the system, from name to specifier.
        :param domain_suffix:
                    The domain-suffix specifying the domain.
        :param domain_code:
                    The domain-code specified by the suffix.
        :param bound:
                    The bound which should be checked against the domain.
        :param stage_type:
                    The type of stage that has the domain-suffix in its name.
        :param stage_name:
                    The name of the stage.
        :param exact:
                    Whether the bound should allow only the domain, or, if False,
                    may allow other domains as well.
        :return:
                    None if the bound matches the domain, or a reason if it doesn't.
        """
        # Make sure the bound on the stage is the instance-type for the suffixed domain
        if exact:
            single_bound = bound.as_single
            if single_bound is None or single_bound.domain_specifier() is not domain_specifier:
                return (
                    f"{stage_type}-stage plugin name contains domain suffix {self}, "
                    f"which contains domain-code '{domain_code}' (domain-code for {domain_specifier.name()}), "
                    f"but it is not solely bound by the domain's instance-type "
                    f"({domain_specifier.instance_type().__name__}). It is instead bound by {bound}."
                )
        else:
            domain_instance_type = domain_specifier.instance_type()
            if bound.intersection_bound(InstanceTypeBoundUnion(domain_instance_type)) is None:
                return (
                    f"{stage_type}-stage plugin name contains domain suffix {self}, "
                    f"which contains domain-code '{domain_code}' (domain-code for {domain_specifier.name()}), "
                    f"but its bound ({bound}) does not accept the domain's instance-type "
                    f"({domain_instance_type.__name__})."
                )

        return None
