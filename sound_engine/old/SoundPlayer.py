import sounddevice as sd
import numpy as np
import librosa
import threading


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
            # sd.wait()
            print(f"Finished playing: {self.name}")
        except Exception as e:
            print(f"Error during playback of {self.name}: {e}")
        finally:
            self._playback_thread = None  # Reset the thread

    def set_volume(self, volume: float):
        volume = np.clip(volume, 0.0, 1.0)
        sound = self.original_sound.copy()

        # Scale amplitude
        self.sound = sound * (volume * 1.0)

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
        scaled_value = np.clip(value, 0.0125, 1.0) * 2
        self.sample_rate = self.original_sound_sample_rate * scaled_value

    def set_sample_length(self, desired_duration: float):
        """Set playback length in seconds using original_sound as base."""
        samples_needed = int(desired_duration * self.sample_rate)
        sound = self.original_sound.copy()

        # Convert mono to stereo if needed
        if sound.ndim == 1:
            sound = np.stack([sound, sound], axis=-1)

        current_samples = sound.shape[0]

        if current_samples > samples_needed:
            sound = sound[:samples_needed, :]
        elif current_samples < samples_needed:
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
