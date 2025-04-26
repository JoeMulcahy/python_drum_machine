######################################################################################
##  Audio file playback
##      -.wav
##      -.mp3 note: mp3 play needs additional libraries to be installed (TODO)
######################################################################################
import numpy as np
import scipy
from pydub import AudioSegment

from app_enums.SoundType import SoundType
from sound_engine.old.SoundPlayer import SoundPlayer


class AudioFile(SoundPlayer):
    def __init__(self, name, filename):
        self.extension = None
        self.filename = filename
        self.determine_file_type()
        super().__init__(name, SoundType.SOUND_SAMPLE, self.sound, self.sample_rate)

    def determine_file_type(self):
        self.extension = self.filename.split('.')[-1]
        if self.extension.lower() == 'mp3':
            # self.get_converted_mp3_as_wav()
            print('mp3 found')
        elif self.extension.lower() == 'wav':
            self.get_sound_data_and_sample_rate_from_wav()

    def get_sound_data_and_sample_rate_from_wav(self):
        self.sample_rate, self.sound = scipy.io.wavfile.read(self.filename)

        # Normalize to [-1.0, 1.0] based on the data's maximum possible value
        if self.sound.dtype == np.int16:
            self.sound = self.sound / 32767.0
        elif self.sound.dtype == np.int32:
            self.sound = self.sound / 2147483647.0
        # Add more conditions for other integer types if necessary
        elif self.sound.dtype == np.float32:
            # Already in float range, but might need to be clipped just in case
            self.sound = np.clip(self.sound, -1.0, 1.0)
        else:
            print(f"Warning: Unknown audio data type: {self.sound.dtype}. Attempting to convert to float.")
            self.sound = self.sound.astype(np.float32)
            self.sound = np.clip(self.sound, -1.0, 1.0)

        # Ensure it's at least 2D for stereo (or mono with a second dimension)
        if self.sound.ndim == 1:
            self.sound = np.stack([self.sound, self.sound], axis=-1)

        self.original_sound = self.sound.copy()  # Update the original sound with normalized data

    def get_converted_mp3_as_wav(self):
        # Load MP3 and convert to raw data
        audio = AudioSegment.from_file(self.filename, format="mp3")
        audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)  # Optional normalization

        # Convert to NumPy array
        self.sound = np.array(audio.get_array_of_samples()).reshape((-1, audio.channels))

        # Normalize to float32 (-1.0 to 1.0) if needed
        self.sound = self.sound.astype(np.float32) / (2 ** 15)