from typing import Iterator, List, Tuple, Union

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....core.util import InstanceState
from ....domain.image.object_detection import ImageObjectDetectionInstance


TYPE_BOOL = "bool"
TYPE_NUMERIC = "numeric"
TYPE_STRING = "string"
TYPES = [
    TYPE_BOOL,
    TYPE_NUMERIC,
    TYPE_STRING,
]
TYPE_BOOL_ID = 0
TYPE_NUMERIC_ID = 1
TYPE_STRING_ID = 2
TYPE_IDS = {
    TYPE_BOOL: TYPE_BOOL_ID,
    TYPE_NUMERIC: TYPE_NUMERIC_ID,
    TYPE_STRING: TYPE_STRING_ID,
}

COMPARISON_L = 0
COMPARISON_LEQ = 1
COMPARISON_EQ = 2
COMPARISON_NEQ = 3
COMPARISON_GEQ = 4
COMPARISON_G = 5
COMPARISONS = {
    "=": COMPARISON_EQ,
    "==": COMPARISON_EQ,
    "!=": COMPARISON_NEQ,
    "<>": COMPARISON_NEQ,
    "<": COMPARISON_L,
    "<=": COMPARISON_LEQ,
    ">": COMPARISON_G,
    ">=": COMPARISON_GEQ,
}


class FilterMetadata(
    RequiresNoFinalisation,
    ProcessorComponent[
        ImageObjectDetectionInstance,
        ImageObjectDetectionInstance
    ]
):
    """
    Processes a stream of image object-detection instances,
    filtering out labels.
    """
    key: str = TypedOption(
        "-k", "--key",
        type=str,
        help="the key of the meta-data value to use for the filtering"
    )

    value_type: str = TypedOption(
        "-t", "--value-type",
        type=str,
        help="the data type that the value represents, available options: %s" % "|".join(TYPES)
    )

    comparison: str = TypedOption(
        "-c", "--comparison",
        type=str,
        help="the comparison to apply to the value: for bool/numeric/string '=OTHER' and '!=OTHER' can be used, " 
             "for numeric furthermore '<OTHER', '<=OTHER', '>=OTHER', '>OTHER'. "
             "E.g.: '<3.0' for numeric types will discard any annotations that have a value of 3.0 or larger"
    )

    @InstanceState
    def _comparison_str(self) -> str:
        comparison = self.comparison
        result = None
        for comparison_str in COMPARISONS:
            if comparison.startswith(comparison_str) and result is None or len(comparison_str) > len(result):
                result = comparison_str


        if result is None:
            raise Exception("Unhandled comparison: %s" % self.comparison)

        return result

    @InstanceState
    def _comparison(self) -> int:
        return COMPARISONS[self._comparison_str]

    @InstanceState
    def _value_type(self) -> int:
        return TYPE_IDS[self.value_type]

    @InstanceState
    def _comparison_value(self) -> Union[bool, float, str]:
        value = self.comparison[len(self._comparison_str):]
        if self._value_type == TYPE_BOOL_ID:
            return bool(value)
        elif self._value_type == TYPE_NUMERIC_ID:
            return float(value)
        else:
            return value

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        located_objects = element.annotation
        if located_objects is not None:
            self.filter_objects(located_objects)

        # no annotations left? -> mark as negative
        if len(located_objects) == 0:
            element = ImageObjectDetectionInstance(element.key, element.data, None)

        then(element)

    def filter_objects(self, objects: LocatedObjects):
        to_remove: List[int] = []
        enumerated: Iterator[Tuple[int, LocatedObject]] = enumerate(objects)
        for i, lobj in enumerated:
            if self.key not in lobj.metadata:
                to_remove.append(i)
            else:
                value = lobj.metadata[self.key]
                try:
                    # bool
                    if self._value_type == TYPE_BOOL_ID:
                        value = bool(value)
                        if self._comparison == COMPARISON_EQ:
                            if value != self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_NEQ:
                            if value == self._comparison_value:
                                to_remove.append(i)
                        else:
                            self.logger.error("Invalid comparison type: %s" % self._comparison_str)
                    # numeric
                    elif self._value_type == TYPE_NUMERIC_ID:
                        value = float(value)
                        if self._comparison == COMPARISON_EQ:
                            if value != self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_NEQ:
                            if value == self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_L:
                            if not (value < self._comparison_value):
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_LEQ:
                            if not (value <= self._comparison_value):
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_G:
                            if not (value > self._comparison_value):
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_GEQ:
                            if not (value >= self._comparison_value):
                                to_remove.append(i)
                        else:
                            self.logger.error("Invalid comparison type: %s" % self._comparison_str)
                    # string
                    elif self._value_type == TYPE_STRING_ID:
                        if self._comparison == COMPARISON_EQ:
                            if value != self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_NEQ:
                            if value == self._comparison_value:
                                to_remove.append(i)
                        else:
                            self.logger.error("Invalid comparison type: %s" % self._comparison_str)
                    else:
                        self.logger.error("Unhandled value type: %s" % self.value_type)
                        return
                except:
                    self.logger.error("Failed to compare: %s" % str(value), exc_info=True)
                    to_remove.append(i)

        # remove objects that didn't meet criteria
        if len(to_remove) > 0:
            for i in reversed(to_remove):
                objects.pop(i)