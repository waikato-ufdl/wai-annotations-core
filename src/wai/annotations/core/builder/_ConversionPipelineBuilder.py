import itertools
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple, Type, Union

from wai.common.cli import OptionsList

from ..domain.specifier import DomainSpecifier
from ..logging import LoggingEnabled, StreamLogger, get_library_root_logger
from ..plugin import get_all_plugins_by_type
from ..plugin.error import BadPluginName
from ..plugin.names import StagePluginName
from ..plugin.names.domain_suffix import DomainCode
from ..stage.bounds import InstanceTypeBoundUnion, InstanceTypeBoundRelationship
from ..stage.specifier import SourceStageSpecifier, ProcessorStageSpecifier, SinkStageSpecifier, StageSpecifier
from ..stage.specifier.validation import (
    validate_source_stage_components,
    validate_processor_stage_components,
    validate_sink_stage_components
)
from ..stage.util import instantiate_stage_as_pipeline
from ..stream import Pipeline
from .error import BadStageName, InputStageNotFirst, StageAfterOutput, StageInvalidForOutputBounds
from ._InlineDomainValidator import InlineDomainValidator


ALL_PLUGINS_BY_TYPE = get_all_plugins_by_type()
DOMAINS: Dict[DomainCode, Type[DomainSpecifier]] = {
    domain_plugin_name.domain_code: domain_specifier
    for domain_plugin_name, domain_specifier in ALL_PLUGINS_BY_TYPE.domains.items()
}
VALID_STAGE_NAMES: Dict[StagePluginName, StagePluginName] = {}
DOMAIN_SUFFIXED_STAGE_NAMES: Dict[StagePluginName, StagePluginName] = {}
INVALID_STAGE_NAMES: Dict[StagePluginName, str] = {}
for item in itertools.chain(
    ALL_PLUGINS_BY_TYPE.source_stages.items(),
    ALL_PLUGINS_BY_TYPE.processor_stages.items(),
    ALL_PLUGINS_BY_TYPE.sink_stages.items()
):
    stage_name: StagePluginName = item[0]
    stage_specifier: Type[StageSpecifier] = item[1]
    VALID_STAGE_NAMES[stage_name] = stage_name
    for with_domain_suffix, reason in stage_name.with_all_domain_suffices(stage_specifier, DOMAINS):
        if reason is None:
            DOMAIN_SUFFIXED_STAGE_NAMES[with_domain_suffix] = with_domain_suffix
        else:
            INVALID_STAGE_NAMES[with_domain_suffix] = reason


@dataclass
class SourceStageSpec:
    name: StagePluginName
    specifier: Type[SourceStageSpecifier]
    bound: InstanceTypeBoundUnion
    options: OptionsList


@dataclass
class ProcessorStageSpec:
    name: StagePluginName
    specifier: Type[ProcessorStageSpecifier]
    bound_relationship: InstanceTypeBoundRelationship
    options: OptionsList


@dataclass
class SinkStageSpec:
    name: StagePluginName
    specifier: Type[SinkStageSpecifier]
    bound: InstanceTypeBoundUnion
    options: OptionsList


class ConversionPipelineBuilder(LoggingEnabled):
    """
    Incrementally builds a complete conversion pipeline. Consists of a source stage,
    a variable number of processor stages and a sink stage, all optional, but
    added in that order i.e. you can't add a source stage after a processor stage
    has already been added. Also provides utilities for constructing a pipeline
    from a command-line.
    """

    def __init__(self):
        # The component stages in the conversion chain
        self._source: Optional[SourceStageSpec] = None
        self._processors: List[ProcessorStageSpec] = []
        self._sink: Optional[SinkStageSpec] = None

    @classmethod
    def split_options(
            cls,
            options: OptionsList,
            *,
            skip_global: bool = False
    ) -> Tuple[OptionsList, List[Tuple[StagePluginName, OptionsList]]]:
        """
        Splits the options list into sub-lists, one for each stage, and the global options.

        :param options:
                    The options list.
        :param skip_global:
                    Whether to skip the global options.
        :return:
                    A pair of:
                     - The global options, and
                     - A list of the options for each stage.
        """
        # Add each stage from the options list
        global_options: OptionsList = []
        stage_options: List[Tuple[StagePluginName, OptionsList]] = []
        for option in options:
            # Handle any initial (global) options
            if (
                    len(stage_options) == 0
                    and option not in VALID_STAGE_NAMES
                    and option not in DOMAIN_SUFFIXED_STAGE_NAMES
                    and option not in INVALID_STAGE_NAMES
            ):
                if not skip_global:
                    global_options.append(option)
                continue

            if option in INVALID_STAGE_NAMES:
                raise BadStageName(f"Invalid domain suffix: {INVALID_STAGE_NAMES[option]}")

            # If we've come across a new stage, add a new sub-options list
            if option in VALID_STAGE_NAMES:
                stage_options.append((VALID_STAGE_NAMES[option], []))
            elif option in DOMAIN_SUFFIXED_STAGE_NAMES:
                stage_options.append((DOMAIN_SUFFIXED_STAGE_NAMES[option], []))
            else:
                stage_options[-1][1].append(option)

        return global_options, stage_options

    @classmethod
    def from_options(
            cls,
            options: Union[OptionsList, List[Tuple[StagePluginName, OptionsList]]]
    ) -> Pipeline:
        """
        Creates a conversion chain from command-line options.

        :param options:     The command-line options.
        :return:            The conversion chain.
        """
        # Split the stage options, if not already
        if len(options) == 0 or isinstance(options[0], tuple):
            stage_option_lists = options
        else:
            _, stage_option_lists = cls.split_options(options, skip_global=True)

        # Create the empty conversion chain
        conversion_chain = ConversionPipelineBuilder()

        # Add each stage from the options list
        for stage_name, stage_options in stage_option_lists:
            conversion_chain.add_stage(stage_name, stage_options)

        return conversion_chain.to_pipeline()

    def add_stage(
            self,
            name: StagePluginName,
            options: OptionsList
    ):
        """
        Adds a stage to the conversion chain.

        :param stage:       The stage to add.
        :param options:     The options to initialise the stage with.
        """
        # Log that we've created the stage
        # TODO: Logging
        #self.logger.info(
        #    f"Created {specifier_type_string(stage_specifier)} stage "
        #    f"of type '{stage}' "
        #    f"with options: {options}"
        #)

        # Add the stage to the overall pipeline
        if name in ALL_PLUGINS_BY_TYPE.source_stages or name.without_domain_suffix in ALL_PLUGINS_BY_TYPE.source_stages:
            self.add_source_stage(name, options)
        elif name in ALL_PLUGINS_BY_TYPE.processor_stages or name.without_domain_suffix in ALL_PLUGINS_BY_TYPE.processor_stages:
            self.add_processor_stage(name, options)
        elif name in ALL_PLUGINS_BY_TYPE.sink_stages or name.without_domain_suffix in ALL_PLUGINS_BY_TYPE.sink_stages:
            self.add_sink_stage(name, options)

    def to_pipeline(self) -> Pipeline:
        """
        Exports the built pipeline.
        """
        # Degenerate state: no stages added
        if self._source is None and len(self._processors) == 0 and self._sink is None:
            return Pipeline()

        # Create local state for the actual components of the final pipeline
        source = None
        processors = []
        sink = None

        # Add the source components if any
        if self._source is not None:
            single_bound = self._source.bound.as_single
            if single_bound is None:
                # TODO: Typed Exception
                raise Exception("Under-specified")
            source_components = self._source.specifier.components(single_bound.domain_specifier())
            validate_source_stage_components(source_components)
            source_pipeline = instantiate_stage_as_pipeline(self._source.specifier, source_components, self._source.options)
            source = source_pipeline.source
            processors += source_pipeline.processors
            if len(self._processors) == 0 and self._sink is None:
                processors.append(InlineDomainValidator(self._source.bound))

        # Add input domain validation and logging
        processors.append(
            StreamLogger(
                get_library_root_logger().info,
                lambda instance: f"Sourced {instance.key}"
            )
        )

        # Add any processors with domain validation
        for processor in self._processors:
            processor_components = processor.specifier.components(processor.bound_relationship)
            validate_processor_stage_components(processor_components)
            processor_pipeline = instantiate_stage_as_pipeline(processor.specifier, processor_components, processor.options)
            processors.append(InlineDomainValidator(processor.bound_relationship.input_bound))
            processors += processor_pipeline.processors
            if processor is self._processors[-1] and self._sink is None:
                processors.append(InlineDomainValidator(processor.bound_relationship.output_bound))

        # Add logging to the pipeline to report when an instance is consumed
        processors.append(
            StreamLogger(
                get_library_root_logger().info,
                lambda instance: f"Consuming {instance.key}"
            )
        )

        # Add the sink
        if self._sink is not None:
            single_bound = self._sink.bound.as_single
            if single_bound is None:
                # TODO: Typed Exception
                raise Exception("Under-specified")
            sink_components = self._sink.specifier.components(single_bound.domain_specifier())
            validate_sink_stage_components(sink_components)
            sink_pipeline = instantiate_stage_as_pipeline(self._sink.specifier, sink_components, self._sink.options)
            processors.append(InlineDomainValidator(self._sink.bound))
            processors += sink_pipeline.processors
            sink = sink_pipeline.sink

        return Pipeline(
            source=source,
            processors=processors,
            sink=sink
        )

    def add_source_stage(
            self,
            name: StagePluginName,
            options: OptionsList
    ):
        """
        Adds a source stage to the pipeline.

        :param stage_specifier:
                    The specifier for the source stage.
        :param stage_pipeline:      The instantiated pipeline for the source stage.
        """
        # Source stage must be added first
        if self._source is not None or len(self._processors) > 0 or self._sink is not None:
            raise InputStageNotFirst()

        stage_specifier = ALL_PLUGINS_BY_TYPE.source_stages.get(
            name if name in VALID_STAGE_NAMES else name.without_domain_suffix,
            None
        )

        if stage_specifier is None:
            raise BadPluginName(str(name), f"Source stage not found")

        source_output_bound = stage_specifier.bound()

        if name.has_domain_suffix:
            reason = name.is_valid_for_stage_specifier(stage_specifier, DOMAINS, exact=False)
            if reason is not None:
                raise BadPluginName(str(name), reason)
            domain = DOMAINS[name.domain_suffix.source_or_sink_domain_code]
            source_output_bound = source_output_bound.intersection_bound(
                InstanceTypeBoundUnion.for_domain(domain)
            )

        # Add the source-stage's components to the overall pipeline
        self._source = SourceStageSpec(name, stage_specifier, source_output_bound, list(options))

    def add_processor_stage(
            self,
            name: StagePluginName,
            options: OptionsList
    ):
        """
        Adds a processor stage to the pipeline.

        :param stage_specifier:     The specifier for the processor stage.
        :param stage_pipeline:      The instantiated pipeline for the processor stage.
        """
        # Processor stage must be added before the sink
        if self._sink is not None:
            raise StageAfterOutput()

        stage_specifier = ALL_PLUGINS_BY_TYPE.processor_stages.get(
            name if name in VALID_STAGE_NAMES else name.without_domain_suffix,
            None
        )

        if stage_specifier is None:
            raise BadPluginName(str(name), f"Processor stage not found")

        bound_relationship = stage_specifier.bound_relationship()

        if name.has_domain_suffix:
            # Check the domain suffix is applicable to the stage
            reason = name.is_valid_for_stage_specifier(stage_specifier, DOMAINS, exact=False)
            if reason is not None:
                raise BadPluginName(str(name), reason)

            # Limit the bound relationship to the suffixed domain-codes
            input_domain_code, output_domain_code = name.domain_suffix.processor_domain_codes
            if input_domain_code is not None:
                bound_relationship = bound_relationship.intersect_input_bound(
                    InstanceTypeBoundUnion.for_domain(DOMAINS[input_domain_code])
                )
            if output_domain_code is not None:
                bound_relationship = bound_relationship.intersect_output_bound(
                    InstanceTypeBoundUnion.for_domain(DOMAINS[output_domain_code])
                )

        # Limit the input to the pipeline's current output
        current_input_bound = bound_relationship.input_bound
        bound_relationship = bound_relationship.intersect_input_bound(self.get_output_bound())
        if bound_relationship is None:
            raise StageInvalidForOutputBounds(name, current_input_bound, self.get_output_bound())

        # Perform a reverse pass to remove now-invalid domains from the processor
        # transfer maps
        self._perform_reverse_pass(name, bound_relationship.input_bound)

        # Add the stage to the overall pipeline
        self._processors.append(ProcessorStageSpec(name, stage_specifier, bound_relationship, list(options)))

    def add_sink_stage(
            self,
            name: StagePluginName,
            options: OptionsList
    ):
        """
        Adds a sink stage to the pipeline.

        :param stage_specifier:     The specifier for the sink stage.
        :param stage_pipeline:      The instantiated pipeline for the sink stage.
        """

        if self._sink is not None:
            raise StageAfterOutput()

        stage_specifier = ALL_PLUGINS_BY_TYPE.sink_stages.get(
            name if name in VALID_STAGE_NAMES else name.without_domain_suffix,
            None
        )

        if stage_specifier is None:
            raise BadPluginName(str(name), f"Sink stage not found")

        sink_input_bound = stage_specifier.bound()

        if name.has_domain_suffix:
            reason = name.is_valid_for_stage_specifier(stage_specifier, DOMAINS, exact=False)
            if reason is not None:
                raise BadPluginName(str(name), reason)
            domain = DOMAINS[name.domain_suffix.source_or_sink_domain_code]
            sink_input_bound = sink_input_bound.intersection_bound(
                InstanceTypeBoundUnion.for_domain(domain)
            )

        # Limit the input to the pipeline's current output
        current_input_bound = sink_input_bound
        sink_input_bound = sink_input_bound.intersection_bound(self.get_output_bound())
        if sink_input_bound is None:
            raise StageInvalidForOutputBounds(name, current_input_bound, self.get_output_bound())

        # Perform a reverse pass to remove now-invalid domains from the processor
        # transfer maps
        self._perform_reverse_pass(name, sink_input_bound)

        # Add the sink-stage's components to the overall pipeline
        self._sink = SinkStageSpec(name, stage_specifier, sink_input_bound, list(options))

    def get_output_bound(self) -> Optional[InstanceTypeBoundUnion]:
        """
        Gets the bounds on the types of instances that the pipeline would
        produce in its current configuration.
        """
        return (
            None if self._sink is not None
            else self._processors[-1].bound_relationship.output_bound if len(self._processors) > 0
            else self._source.bound if self._source is not None
            else InstanceTypeBoundUnion.any()
        )

    def _perform_reverse_pass(
            self,
            name: StagePluginName,
            required_output_bound: InstanceTypeBoundUnion
    ):
        """
        Performs a reverse-pass over the transfer maps of the processor stages,
        ensuring that each stage only passes domains that can cause the pipeline
        to end in one of the given domains.

        :param allowed_output_domains:  The set of allowed domains at the end of the pipeline.
        """
        # Process each processor stage in reverse order
        next_bound = required_output_bound
        for processor_stage in reversed(self._processors):
            bound_relationship = processor_stage.bound_relationship

            bound_relationship = bound_relationship.intersect_output_bound(next_bound)

            if bound_relationship is None:
                # TODO: Typed exception
                raise Exception(
                    f"Stage '{name}' failed reverse pass"
                )

            processor_stage.bound_relationship = bound_relationship

            next_bound = bound_relationship.input_bound

        if self._source is not None:
            bound = self._source.bound
            bound = bound.intersection_bound(next_bound)
            if bound is None:
                # TODO: Typed exception
                raise Exception(
                    f"Stage '{name}' failed reverse pass"
                )
            self._source.bound = bound

