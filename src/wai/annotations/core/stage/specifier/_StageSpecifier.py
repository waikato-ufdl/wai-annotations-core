from typing import Union

from ._ProcessorStageSpecifier import ProcessorStageSpecifier
from ._SinkStageSpecifier import SinkStageSpecifier
from ._SourceStageSpecifier import SourceStageSpecifier

StageSpecifier = Union[
    SourceStageSpecifier,
    ProcessorStageSpecifier,
    SinkStageSpecifier
]
