import sounddevice as sd
import numpy as np
import scipy.io.wavfile
from pydub import AudioSegment
import librosa
import threading

from sound_engine.SoundType import SoundType


class SoundPlayer:
    def __init__(self, name, mode, sound, sample_rate=44100):
        self.name = name
        self.mode = mode
        self.original_sound = sound.copy()
        self.sound = sound.copy()
        self.original_sound_sample_rate = sample_rate
        self.sample_rate = self.original_sound_sample_rate
        self._playback_thread = None  # To keep track of the playback thread

    def play(self):
        if self._playback_thread and self._playback_thread.is_alive():
            print(f"Warning: {self.name} is already playing.")
            return

        self._playback_thread = threading.Thread(target=self._play_audio)
        self._playback_thread.start()
        print(f"Started playback of: {self.name} on a new thread.")

    def _play_audio(self):
        try:
            sd.play(self.sound, self.sample_rate)
            sd.wait()
            print(f"Finished playing: {self.name}")
        except Exception as e:
            print(f"Error during playback of {self.name}: {e}")
        finally:
            self._playback_thread = None  # Reset the thread

    def set_volume(self, volume: float):
        # print(f"Input: {volume}")
        volume = np.clip(volume, 0.0, 1.0)
        # print(f"Input clip: {volume}")
        sound = self.original_sound.copy()

        # Scale amplitude
        self.sound = sound * (volume * 1.0)
        # print(f"Min value after volume scaling: {np.min(self.sound)}")
        # print(f"Max value after volume scaling: {np.max(self.sound)}")

    def set_pan(self, pan_value: float):
        """Pan audio between -1.0 (left) and 1.0 (right), using original_sound as base."""
        print(f"Input: {pan_value}")
        sound = self.original_sound.copy()

        # Convert mono to stereo if needed
        if sound.ndim == 1:
            sound = np.stack([sound, sound], axis=-1)

        # Clamp pan to [-1.0, 1.0]
        pan_value = pan_value * 2 - 1
        pan_value = np.clip(pan_value, -1.0, 1.0)
        print(f"Scaled: {pan_value}")

        # Equal-power panning
        left_gain = np.cos((pan_value + 1) * np.pi / 4)
        right_gain = np.sin((pan_value + 1) * np.pi / 4)

        sound[:, 0] *= left_gain
        sound[:, 1] *= right_gain

        self.sound = sound

    def set_sample_rate(self, value: float):
        """Change the sample rate for playback (scales the current rate)."""
        print(f"original rate: {self.original_sound_sample_rate}")
        scaled_value = np.clip(value, 0.0125, 1.0) * 2
        print(f"Scaled: {scaled_value}")
        self.sample_rate = self.original_sound_sample_rate * scaled_value
        print(f"scaled value: {scaled_value}")
        print(f"new sample rate: {self.sample_rate}")

    def set_sample_length(self, desired_duration: float):
        """Set playback length in seconds using original_sound as base."""
        samples_needed = int(desired_duration * self.sample_rate)
        sound = self.original_sound.copy()

        # Convert mono to stereo if needed
        if sound.ndim == 1:
            sound = np.stack([sound, sound], axis=-1)

        current_samples = sound.shape[0]

        if current_samples > samples_needed:
            # Truncate
            sound = sound[:samples_needed, :]
        elif current_samples < samples_needed:
            # Pad with zeros
            padding = np.zeros((samples_needed - current_samples, sound.shape[1]), dtype=sound.dtype)
            sound = np.vstack((sound, padding))

        self.sound = sound

    def set_sample_duration(self, duration):
        duration = np.clip(duration, 0.0,
                           1.0)  # Input is likely from a UI element scaled 0-100%, so this should be 0.0 to 1.0
        duration = duration * 3
        self.sound = self.original_sound.copy()  # Reset to the original sound data
        current_duration_samples = self.sound.shape[0]  # Get the number of samples in the original sound
        if duration <= 0:  # Avoid division by zero
            self.sound = np.zeros_like(self.original_sound)  # Or handle this case differently
            return

        # Calculate the desired duration in seconds based on the 0.0-1.0 UI input
        # Assuming the UI's 0.0-1.0 represents a multiplier of the original duration
        desired_duration_seconds = duration * (current_duration_samples / self.sample_rate)
        desired_num_samples = int(desired_duration_seconds * self.sample_rate)

        if desired_num_samples <= 0:
            self.sound = np.zeros_like(self.original_sound)
            return

        # Time stretch using librosa
        temp_sound = self.sound.copy()
        if temp_sound.ndim == 2:
            temp_sound = librosa.to_mono(temp_sound.T)

        # Calculate the stretch ratio based on the desired number of samples
        stretch_ratio = current_duration_samples / desired_num_samples

        stretched = librosa.effects.time_stretch(temp_sound, rate=stretch_ratio)

        # Convert back to stereo
        if self.original_sound.ndim == 2:
            stereo_stretched = np.stack([stretched, stretched], axis=-1)
            self.sound = stereo_stretched
        else:
            self.sound = stretched  # Keep it mono if the original was mono


######################################################################################
##  Audio file playback
##      -.wav
##      -.mp3 note: mp3 play needs additional libraries to be installed (TODO)
######################################################################################

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
        # self.sound = self.sound.astype(np.float32)

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


######################################################################################
##  Basic Sound Wave Generation
##      -Sin
##      -Square
##      -Triangle
##      -Noise ---(TODO)---
######################################################################################

class SoundWave(SoundPlayer):
    def __init__(self, name, frequency, duration, volume, sample_rate, wave_form):
        self.frequency = frequency
        self.duration = duration
        self.volume = volume
        self.sample_rate = sample_rate
        self.wave_form = wave_form
        self.sound = self.get_waveform()
        self.sound = self.sound.astype(np.float32) / 32768.0
        super().__init__(name, SoundType.SOUND_WAVE, self.sound, sample_rate)

    def get_waveform(self):
        # Placeholder: to be overridden by subclasses
        return np.zeros(int(self.sample_rate * self.duration))


class SinWave(SoundWave):
    def __init__(self, name, frequency, duration, volume, sample_rate):
        self.frequency = frequency
        self.duration = duration
        self.volume = volume
        self.sample_rate = sample_rate
        super().__init__(name, frequency, duration, volume, sample_rate, wave_form="sine")

    def get_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        return self.volume * np.sin(2 * np.pi * self.frequency * t)


class SquareWave(SoundWave):
    def __init__(self, name, frequency, duration, volume, sample_rate):
        self.frequency = frequency
        self.duration = duration
        self.sample_rate = sample_rate
        super().__init__(name, frequency, duration, volume, sample_rate, wave_form="square")

    def get_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        return self.volume * np.sign(np.sin(2 * np.pi * self.frequency * t))


class TriangleWave(SoundWave):
    def __init__(self, name, frequency, duration, volume, sample_rate):
        self.frequency = frequency
        self.duration = duration
        self.sample_rate = sample_rate
        super().__init__(name, frequency, duration, volume, sample_rate, wave_form="triangle")

    def get_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        return self.volume * (2 * np.abs(2 * (t * self.frequency - np.floor(t * self.frequency + 0.5))) - 1)
