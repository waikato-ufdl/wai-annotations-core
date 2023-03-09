from abc import ABC, abstractmethod
from random import Random
from typing import Optional

from wai.common.cli.options import TypedOption, Option

from ...stream.util import ProcessState
from .._Component import Component


class WithRandomness(Component, ABC):
    """
    Adds a seed option to a component, and automatically provides
    a source of randomness for instances to use.
    """
    # The seed to use for randomisation of the read sequence
    seed: Optional[int] = TypedOption(
        "--seed",
        type=int
    )

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.seed:
            return cls.get_help_text_for_seed_option()
        return super().get_help_text_for_option(option)

    @classmethod
    @abstractmethod
    def get_help_text_for_seed_option(cls) -> str:
        raise NotImplementedError(cls.get_help_text_for_seed_option.__qualname__)


class WithOptionalRandomness(WithRandomness):
    """
    Mixin for components where randomness can be utilised if selected,
    but is not required. E.g. a component which shuffles the order of
    items if provided with a source of randomness, or leaves the order
    untouched if not.
    """
    # The source of randomness for the component
    random: Optional[Random] = ProcessState(lambda self: None if self.seed is None else Random(self.seed))

    @property
    def has_random(self):
        """
        Whether a seed was provided.
        """
        return self.random is not None

    @classmethod
    def get_help_text_for_seed_option(cls) -> str:
        return "the seed to use for randomisation (default: no randomisation)"

class WithPossiblySeededRandomness(WithRandomness):
    """
    Mixin for components which require a source of randomness. As opposed to
    WithOptionalRandomness, if no seed is provided, Random's default seeding
    is used (current time).
    """
    # The source of randomness for the component
    random: Random = ProcessState(lambda self: Random(self.seed))

    @classmethod
    def get_help_text_for_seed_option(cls) -> str:
        return "the seed to use for randomisation (default: seeded by current time)"
