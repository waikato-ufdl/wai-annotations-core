from typing import Type, TYPE_CHECKING

from ...util import is_subtype

if TYPE_CHECKING:
    from ..specifier import StageSpecifier

def stage_specifier_base_type(
        specifier: Type['StageSpecifier']
) -> Type['StageSpecifier']:
    """
    Returns the base specifier-type of the stage the given specifier specifies.

    :param specifier:
                The stage specifier.
    :return:
                The specifier base-type
    """
    from ..specifier import ProcessorStageSpecifier, SinkStageSpecifier, SourceStageSpecifier

    if is_subtype(specifier, ProcessorStageSpecifier):
        return ProcessorStageSpecifier
    elif is_subtype(specifier, SinkStageSpecifier):
        return SinkStageSpecifier
    elif is_subtype(specifier, SourceStageSpecifier):
        return SourceStageSpecifier
    else:
        raise Exception(f"Unknown specifier type: {specifier}")
