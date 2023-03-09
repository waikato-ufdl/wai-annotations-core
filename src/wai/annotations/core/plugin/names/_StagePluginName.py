from typing import Dict, Iterable, Optional, Tuple, Type, TYPE_CHECKING

from .constants import PLUGIN_NAME_MATCHER
from .domain_suffix import DomainSuffix, DomainCode
from ._PluginName import PluginName

if TYPE_CHECKING:
    from ...domain.specifier import DomainSpecifier
    from ...stage.specifier import StageSpecifier

class StagePluginName(PluginName):
    @classmethod
    def _validate_name(cls, name: str) -> Optional[str]:
        if PLUGIN_NAME_MATCHER(name) is None:
            return f"Store plugin name must be dash-separated lowercase letters but was '{name}'"
        return None

    def __init__(
            self,
            name: str,
            for_processor: bool,
            domain_suffix: Optional[DomainSuffix] = None
    ):
        if domain_suffix is None:
            domain_suffix = DomainSuffix.try_parse(name, for_processor)
        else:
            if domain_suffix.for_processor and not for_processor:
                raise Exception("Domain-suffix for processor given for non-processor stage-name")
            elif for_processor and not domain_suffix.for_processor:
                raise Exception("Domain-suffix for non-processor given for processor stage-name")

            name = f"{name}{domain_suffix}"

        super().__init__(name)
        self._domain_suffix = domain_suffix
        self._without_domain_suffix = (
            name[:-len(str(self._domain_suffix))] if self._domain_suffix is not None
            else name
        )

    @property
    def domain_suffix(self) -> Optional[DomainSuffix]:
        return self._domain_suffix

    @property
    def without_domain_suffix(self) -> str:
        return self._without_domain_suffix

    @property
    def has_domain_suffix(self) -> bool:
        return self._domain_suffix is not None

    def with_all_domain_suffices(
            self,
            stage_specifier: Type['StageSpecifier'],
            domains: Dict[DomainCode, Type['DomainSpecifier']]
    ) -> Iterable[Tuple['StagePluginName', Optional[str]]]:
        if self.has_domain_suffix:
            return tuple()

        return (
            (stage_name, stage_name.is_valid_for_stage_specifier(stage_specifier, domains, exact=False))
            for domain_suffix in DomainSuffix.all_domain_suffices(stage_specifier, domains)
            for stage_name in [StagePluginName(self._name, domain_suffix.for_processor, domain_suffix)]
        )

    def is_valid_for_stage_specifier(
            self,
            stage_specifier: Type['StageSpecifier'],
            domains:  Dict[DomainCode, Type['DomainSpecifier']],
            *,
            exact: bool = True
    ) -> Optional[str]:
        return (
            None if self._domain_suffix is None
            else self._domain_suffix.is_valid_for_stage_specifier(
                stage_specifier,
                domains,
                exact=exact
            )
        )
