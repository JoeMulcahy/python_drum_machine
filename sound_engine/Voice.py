import threading
import sounddevice as sd

import librosa
import numpy as np


class Voice:
    def __init__(self, data: np.ndarray, samplerate: int):
        self.__data = data
        self.__data_copy = data
        self.__samplerate = samplerate
        self.__original_sample_rate = samplerate
        self.__position = 0  # Current playback index
        self.__active = True
        self._playback_thread = None  # To keep track of the playback thread

    def next_chunk(self, frames: int) -> np.ndarray:
        if not self.__active:
            return np.zeros((frames, self.__data.shape[1] if self.__data.ndim > 1 else 1), dtype=np.float32)

        if self.__position >= len(self.__data):
            self.__active = False
            return np.zeros((frames, self.__data.shape[1] if self.__data.ndim > 1 else 1), dtype=np.float32)

        end = self.__position + frames
        chunk = self.__data[self.__position:end]

        # Ensure chunk is 2D
        if chunk.ndim == 1:
            chunk = chunk[:, np.newaxis]  # Add a channel dimension
        elif chunk.ndim > 2:
            chunk = chunk.squeeze(axis=1)

        self.__position = end

        # Pad with zeros if end of audio
        if len(chunk) < frames:
            padding = np.zeros((frames - len(chunk), self.__data.shape[1] if self.__data.ndim > 1 else 1),
                               dtype=np.float32)
            chunk = np.concatenate((chunk, padding), axis=0)

        return chunk

    def preview_voice(self):
        if self._playback_thread and self._playback_thread.is_alive():
            print(f"Warning: sound is already playing.")
            return  # Important: Return, don't start a new thread

        self._playback_thread = threading.Thread(target=self.__play_audio)
        self._playback_thread.start()
        print(f"Started playback of: sound on a new thread.")

    def __play_audio(self):
        try:
            sd.play(self.__data_copy, self.__samplerate)
            # sd.wait()  # changed to sd.wait
        except Exception as e:
            print(f"Error during playback of sound: {e}")
        finally:
            self._playback_thread = None  # Reset the thread

    def reset_position(self):
        """Reset the playback position to the beginning of the sound."""
        self.__position = 0
        self.__active = True  # Make sure the voice is active when it is reset

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.__active = value

    @property
    def sample_rate(self):
        return self.__samplerate

    @sample_rate.setter
    def sample_rate(self, value):
        self.__samplerate = value

    def modify_sample_rate(self, value: float):
        """Change the sample rate for playback (scales the current rate)."""
        scaled_value = np.clip(value, 0.0125, 1.0) * 2
        self.__samplerate = self.__original_sample_rate * scaled_value

    def set_sample_length(self, desired_duration: float):
        """Set playback length in seconds using original_sound as base."""
        samples_needed = int(desired_duration * self.sample_rate)
        sound = self.__data_copy.copy()

        # Convert mono to stereo if needed
        if sound.ndim == 1:
            sound = np.stack([sound, sound], axis=-1)

        current_samples = sound.shape[0]

        if current_samples > samples_needed:
            sound = sound[:samples_needed, :]
        elif current_samples < samples_needed:
            padding = np.zeros((samples_needed - current_samples, sound.shape[1]), dtype=sound.dtype)
            sound = np.vstack((sound, padding))

        self.__data = sound

    def set_sample_duration(self, duration_multiplier: float):
        duration_multiplier = np.clip(duration_multiplier, 0.0, 1.0)  # Input between 0.0 to 1.0 from gui dial
        duration = duration_multiplier * 3
        self.__data = self.__data_copy.copy()  # Reset to the original sound data
        current_duration_samples = self.__data.shape[0]  # Get the number of samples in the original sound
        if duration <= 0:  # Avoid division by zero
            self.__data = np.zeros_like(self.__data)  # Or handle this case differently
            return

        # Calculate the desired duration in seconds based on the 0.0-1.0 UI input
        # Assuming the UI's 0.0-1.0 represents a multiplier of the original duration
        desired_duration_seconds = duration * (current_duration_samples / self.__samplerate)
        desired_num_samples = int(desired_duration_seconds * self.__samplerate)

        if desired_num_samples <= 0:
            self.__data = np.zeros_like(self.__data_copy)
            return

        # Time stretch using librosa
        temp_sound = self.__data.copy()
        if temp_sound.ndim == 2:
            temp_sound = librosa.to_mono(temp_sound.T)

        # Calculate the stretch ratio based on the desired number of samples
        stretch_ratio = current_duration_samples / desired_num_samples

        stretched = librosa.effects.time_stretch(temp_sound, rate=stretch_ratio)

        # Convert back to stereo
        if self.__data_copy.ndim == 2:
            stereo_stretched = np.stack([stretched, stretched], axis=-1)
            self.__data = stereo_stretched
        else:
            self.__data = stretched  # Keep it mono if the original was mono





