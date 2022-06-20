import os
import librosa
import tempfile
import time

from wai.annotations.domain.audio import AudioFormat


def load_audio_data(data: bytes, audio_format: AudioFormat, sample_rate: int = None):
    """
    Loads the audio data from the file data.

    :param data: the audio file data
    :param audio_format: the format of the audio data
    :param sample_rate: the sample_rate to use if other than native
    :return: the tuple of audio time series and sample rate
    """
    if audio_format == AudioFormat.MP3:
        filename_tmp = os.path.join(tempfile.gettempdir(), "waiann-%d.mp3" % round(time.time()))
        with open(filename_tmp, "wb") as fp:
            fp.write(data)
            fp.close()
        return librosa.load(filename_tmp, sr=sample_rate, mono=False)
    else:
        return librosa.load(data, sr=sample_rate, mono=False)
