import librosa
import numpy as np

from typing import Optional, Tuple, Type
from ...core.domain import Data
from ._AudioFormat import AudioFormat
from .util import convert_audio_format, load_audio_data

# The default audio-format to use if generating audio file-data from audio-data
DEFAULT_AUDIO_FORMAT: AudioFormat = AudioFormat.OGG


class Audio(Data):
    """
    Contains the information about an audio file.
    """
    def __init__(
            self,
            data: Optional[bytes],
            format: Optional[AudioFormat] = None,
            sample_rate: Optional[int] = None,
            audio_data: Optional[Tuple[np.ndarray, int]] = None,
    ):
        if data is None:
            if audio_data is None:
                raise Exception("Can't create file-data without audio-data")
            if format is None:
                format = DEFAULT_AUDIO_FORMAT

            data = convert_audio_format(audio_data[0], audio_data[1], format)

        super().__init__(data)

        self._format: Optional[AudioFormat] = format
        self._sample_rate: Optional[int] = sample_rate
        self._audio_data: Optional[Tuple[np.ndarray, int]] = audio_data

    @property
    def audio_data(self) -> Tuple[np.ndarray, int]:
        """
        Returns a tuple of the audio data and sample rate.

        :return: the tuple of audio data and sample rate or None if no data available
        """
        if self._audio_data is None:
            self._audio_data = load_audio_data(self._data, self._format, self._sample_rate)
        return self._audio_data

    @property
    def format(self) -> Optional[AudioFormat]:
        """
        Gets the format of this audio file.
        """
        return self._format

    def get_duration(self) -> float:
        """
        Returns the duration in seconds.
        CAUTION: has to read the data if not yet converted to audio_data tuple.

        :return: the duration in seconds.
        """
        return librosa.get_duration(self.audio_data[0], self.audio_data[1])

    def convert(self, to_format: AudioFormat) -> 'Audio':
        """
        Converts this audio file into another format.

        :param to_format:   The audio format to convert to.
        :return:            The converted audio object.
        """
        # If it's the same format, just make a copy
        if to_format is self._format:
            return self

        return Audio(
            None,
            to_format,
            self._sample_rate,
            self.audio_data
        )

    @classmethod
    def from_data(cls: Type['Audio'], file_data: bytes) -> 'Audio':
        return cls(file_data)
