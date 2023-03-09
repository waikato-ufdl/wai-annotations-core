"""
Package of errors that can occur while building a conversion pipeline.
"""
from ._BadDomain import BadDomain
from ._BadStageName import BadStageName
from ._InputStageNotFirst import InputStageNotFirst
from ._StageAfterOutput import StageAfterOutput
from ._StageInvalidForOutputBounds import StageInvalidForOutputBounds
