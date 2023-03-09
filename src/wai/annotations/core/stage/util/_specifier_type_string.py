from typing import Dict, Type, TYPE_CHECKING

from ._stage_specifier_base_type import stage_specifier_base_type

if TYPE_CHECKING:
    from ..specifier import StageSpecifier

SPECIFIER_TYPE_STRINGS: Dict[Type['StageSpecifier'], str] = {}


def specifier_type_string(specifier: Type['StageSpecifier']) -> str:
    """
    Returns a string describing the type of stage the given specifier specifies.

    :param specifier:   The stage specifier.
    :return:            A short name for the type of stage specified.
    """
    global SPECIFIER_TYPE_STRINGS
    if len(SPECIFIER_TYPE_STRINGS) == 0:
        from ..specifier import ProcessorStageSpecifier, SinkStageSpecifier, SourceStageSpecifier
        SPECIFIER_TYPE_STRINGS.update({
            SourceStageSpecifier: "source stage",
            ProcessorStageSpecifier: "processor stage",
            SinkStageSpecifier: "sink stage"
        })

    string = SPECIFIER_TYPE_STRINGS.get(
        stage_specifier_base_type(specifier),
        None
    )

    if string is None:
        raise Exception(f"Unknown specifier type: {specifier}")

    return string
