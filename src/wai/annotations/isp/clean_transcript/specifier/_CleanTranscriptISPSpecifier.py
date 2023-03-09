from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import Data
from ....core.stage.bounds import InstanceTypeBoundRelationship
from ....core.stage.specifier import ProcessorStageSpecifier
from ....domain.audio.speech import Transcription


class CleanTranscriptISPSpecifier(ProcessorStageSpecifier):
    """
    ISP that cleans speech transcripts.
    """
    @classmethod
    def name(cls) -> str:
        return "Clean Transcript"

    @classmethod
    def description(cls) -> str:
        return "ISP that cleans speech transcripts."

    @classmethod
    def bound_relationship(cls) -> InstanceTypeBoundRelationship:
        return InstanceTypeBoundRelationship(
            (Data, Transcription),
            (Data, Transcription),
            input_instance_type_must_match_output_instance_type=True,
            output_instance_type_must_match_input_instance_type=True
        )

    @classmethod
    def components(cls, bound_relationship: InstanceTypeBoundRelationship) -> Tuple[Type[ProcessorComponent]]:
        from ...clean_transcript.component import CleanTranscript
        return CleanTranscript,
