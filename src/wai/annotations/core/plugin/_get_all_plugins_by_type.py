import functools
import itertools
from dataclasses import dataclass, field
from typing import Dict, List, Type, TYPE_CHECKING

from .names import DomainPluginName, StorePluginName, StagePluginName
from .error import BadPluginName, BadPluginSpecifier
from .specifier import PluginSpecifier
from ._get_all_plugins import get_all_plugins

if TYPE_CHECKING:
    from ..domain.specifier import DomainSpecifier
    from ..stage.specifier import SourceStageSpecifier, ProcessorStageSpecifier, SinkStageSpecifier
    from ..store.specifier import StoreSpecifier


@dataclass
class AllPluginsByType:
    domains: Dict[DomainPluginName, Type['DomainSpecifier']] = field(default_factory=lambda: {})
    stores: Dict[StorePluginName, Type['StoreSpecifier']] = field(default_factory=lambda: {})
    source_stages: Dict[StagePluginName, Type['SourceStageSpecifier']] = field(default_factory=lambda: {})
    processor_stages: Dict[StagePluginName, Type['ProcessorStageSpecifier']] = field(default_factory=lambda: {})
    sink_stages: Dict[StagePluginName, Type['SinkStageSpecifier']] = field(default_factory=lambda: {})


def get_all_plugins_by_type() -> AllPluginsByType:
    """
    Gets a mapping from plugin base-type to the plugins
    of that type registered with the system.
    """
    cached = get_all_plugins_by_type_cached()

    return AllPluginsByType(
        domains=dict(cached.domains),
        stores=dict(cached.stores),
        source_stages=dict(cached.source_stages),
        processor_stages=dict(cached.processor_stages),
        sink_stages=dict(cached.sink_stages),
    )


@functools.lru_cache(1)
def get_all_plugins_by_type_cached() -> AllPluginsByType:
    """
    Gets a mapping from plugin base-type to the plugins
    of that type registered with the system.
    """
    from ..domain.specifier import DomainSpecifier
    from ..domain.specifier.validation import validate_domain_specifier
    from ..stage.specifier import SourceStageSpecifier, ProcessorStageSpecifier, SinkStageSpecifier
    from ..stage.specifier.validation import (
        validate_source_stage_specifier,
        validate_processor_stage_specifier,
        validate_sink_stage_specifier
    )
    from ..store.specifier import StoreSpecifier
    from ..store.specifier.validation import validate_store_specifier

    all_base_types: List[Type[PluginSpecifier]] = [
        DomainSpecifier,
        StoreSpecifier,
        SourceStageSpecifier,
        ProcessorStageSpecifier,
        SinkStageSpecifier
    ]

    # Create the empty result object
    all_plugins_by_type: AllPluginsByType = AllPluginsByType()

    # Add each plugin to a set under its base-type
    for name, plugin_specifier in get_all_plugins().items():
        # Make sure the plugin implements exactly one plugin type
        base_types = [
            base_type
            for base_type in all_base_types
            if issubclass(plugin_specifier, base_type)
        ]
        if len(base_types) > 1:
            raise BadPluginSpecifier(
                f"Plugin specifiers should implement exactly one base-type, but "
                f"'{name}' ({plugin_specifier.__qualname__}) "
                f"is a "
                f"{' and a '.join(base_type.__qualname__ for base_type in base_types)}"
            )
        elif len(base_types) == 0:
            raise BadPluginSpecifier(
                f"Plugin specifier '{name}' ({plugin_specifier.__qualname__}) is not a known plugin type"
            )

        # Add this plugin to its base-type group
        if issubclass(plugin_specifier, DomainSpecifier):
            name = DomainPluginName(name)
            try:
                all_plugins_by_type.domains[name] = validate_domain_specifier(plugin_specifier)
            except Exception as e:
                raise BadPluginSpecifier(f"Invalid domain specifier: {e}") from e

        elif issubclass(plugin_specifier, StoreSpecifier):
            name = StorePluginName(name)
            try:
                all_plugins_by_type.stores[name] = validate_store_specifier(plugin_specifier)
            except Exception as e:
                raise BadPluginSpecifier(f"Invalid store specifier: {e}") from e
        else:
            name = StagePluginName(name, issubclass(plugin_specifier, ProcessorStageSpecifier))
            if issubclass(plugin_specifier, SourceStageSpecifier):
                try:
                    all_plugins_by_type.source_stages[name] = validate_source_stage_specifier(plugin_specifier)
                except Exception as e:
                    raise BadPluginSpecifier(f"Invalid source-stage specifier: {e}") from e

            elif issubclass(plugin_specifier, ProcessorStageSpecifier):
                try:
                    all_plugins_by_type.processor_stages[name] = validate_processor_stage_specifier(plugin_specifier)
                except Exception as e:
                    raise BadPluginSpecifier(f"Invalid processor-stage specifier: {e}") from e

            elif issubclass(plugin_specifier, SinkStageSpecifier):
                try:
                    all_plugins_by_type.sink_stages[name] = validate_sink_stage_specifier(plugin_specifier)
                except Exception as e:
                    raise BadPluginSpecifier(f"Invalid sink-stage specifier: {e}") from e

    # Once all domains are loaded, ensure that stage names are valid for their specified stages
    for stage_name, stage_specifier in itertools.chain(
        all_plugins_by_type.source_stages.items(),
        all_plugins_by_type.processor_stages.items(),
        all_plugins_by_type.sink_stages.items()
    ):
        reason = stage_name.is_valid_for_stage_specifier(
            stage_specifier,
            all_plugins_by_type.domains,
            exact=False
        )
        if reason is not None:
            raise BadPluginName(str(stage_name), reason)

    return all_plugins_by_type
