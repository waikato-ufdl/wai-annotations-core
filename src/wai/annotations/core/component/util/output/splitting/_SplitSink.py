import os
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, TypeVar

from wai.bynning.operations import split as bynning_split_op

from wai.common.cli.options import TypedOption, FlagOption

from .....stream.util import ProcessState
from .....util import InstanceState, gcd
from ...._SinkComponent import SinkComponent

ElementType = TypeVar("ElementType")


class SplitSink(
    SinkComponent[ElementType],
    ABC
):
    """
    Base class for classes which can write a specific external format.
    """
    split_names = TypedOption(
        "--split-names",
        type=str,
        metavar="SPLIT NAME",
        nargs="+",
        help="the names to use for the splits"
    )

    split_ratios = TypedOption(
        "--split-ratios",
        type=int,
        metavar="RATIO",
        nargs="+",
        help="the ratios to use for the splits"
    )

    no_interleave = FlagOption(
        "--no-interleave",
        help="disables item interleaving (splitting will occur in runs)"
    )

    def consume_element(self, element: ElementType):
        self.consume_element_for_split(element)
        self._move_to_next_split()

    @abstractmethod
    def consume_element_for_split(self, element: ElementType):
        raise NotImplementedError(self.consume_element_for_split.__qualname__)

    def finish(self):
        # If we're not splitting, just finish the None split
        if not self.is_splitting:
            return self.finish_split()

        # Create a set of finished splits so we don't finish each more than once
        finished_splits = set()

        # Manually move through the splits so we only pass once
        split_index = 0

        # Finish each split
        while split_index < len(self.split_schedule):
            # Manually move to the indexed split
            self.split_index = split_index

            # Finish this split if we haven't already
            if self.split_label not in finished_splits:
                self.finish_split()
                finished_splits.add(self.split_label)

            # Move on to the next split in the schedule
            split_index += 1

    @abstractmethod
    def finish_split(self):
        raise NotImplementedError(self.finish_split.__qualname__)

    @staticmethod
    def format_split_path(
            path: str,
            split_name: Optional[str],
            prefix: bool = False
    ) -> str:
        """
        Formats the path for a split.

        :param path:
                    The base path.
        :param split_name:
                    The name of the split, or None for no split.
        :param prefix:
                    Whether the split-name should appear at the beginning of the path.
                    Default is False, i.e. the split-name should be the last directory element
                    of the path.
        :return:
                    The path for the split.
        """
        # Use the given path if no split-name is given
        if split_name is None:
            return path

        directory, filename = os.path.split(path)
        if prefix:
            return os.path.join(split_name, directory, filename)
        else:
            return os.path.join(directory, split_name, filename)

    @property
    def is_splitting(self) -> bool:
        """
        Whether this writer is performing a split-write.
        """
        return len(self.split_names) != 0 and len(self.split_ratios) != 0

    @InstanceState
    def split_table(self) -> Dict[Optional[str], int]:
        """
        Table from split name to split ratio.
        """
        # If we're not splitting, create a default table
        if not self.is_splitting:
            return {None: -1}

        # Create a table from split-name to split-ratio
        table = {
            split_name: split_ratio
            for split_name, split_ratio
            in zip(self.split_names, self.split_ratios)
        }

        # Reduce each ratio to its lowest form
        table_gcd = gcd(*table.values())
        for split_name in table:
            table[split_name] //= table_gcd

        return table

    @InstanceState
    def split_schedule(self) -> Tuple[str, ...]:
        """
        Creates a schedule of which split to assign elements to
        in order of discovery.
        """
        # If we're not splitting, return an empty schedule
        if not self.is_splitting:
            return tuple()

        # Calculate a range over the length of the schedule
        schedule_range = range(sum(self.split_table.values()))

        # Create a mapping from split-name to schedule indices
        split_indices_by_name = {
            split_name: set(split_indices)
            for split_name, split_indices
            in bynning_split_op(schedule_range, **self.split_table).items()
        }

        # Enables the buggy non-interleaved behaviour (for backwards compatibility)
        if self.no_interleave:
            return tuple(
                split_name
                for split_name, split_indices in split_indices_by_name.items()  # This line...
                for index in schedule_range                                     # ...is swapped with this line
                if index in split_indices
            )

        return tuple(
            split_name
            for index in schedule_range
            for split_name, split_indices in split_indices_by_name.items()
            if index in split_indices
        )

    @ProcessState
    def split_index(self) -> int:
        return 0 if self.is_splitting else -1

    @property
    def split_label(self) -> Optional[str]:
        if not self.is_splitting:
            return None
        return self.split_schedule[self.split_index]

    def _move_to_next_split(self):
        if not self.is_splitting:
            return
        self.split_index = (self.split_index + 1) % len(self.split_schedule)
