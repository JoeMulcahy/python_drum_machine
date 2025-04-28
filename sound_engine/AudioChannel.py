import numpy as np

from sound_engine import Voice


class AudioChannel:
    def __init__(self, channel_id, voice: Voice, volume=1.0, pan=0.0):
        self.__id = channel_id
        self.__voice = voice
        self.__volume = volume  # 0.0 to 1.0
        self.__pan = pan  # -1.0 (L) to 1.0 (R)
        self.is_playing = False  # Add is_playing attribute
        self.start_time = 0  # Add start_time attribute

    def next_stereo_chunk(self, frames: int) -> np.ndarray:
        if not self.is_playing:
            return np.zeros((frames, 2), dtype=np.float32)

        mono = self.__voice.next_chunk(frames) * self.__volume
        if mono.ndim > 1:
            mono = mono.squeeze(axis=1)

        # Simple equal-power panning
        left = mono * np.cos((self.__pan + 1) * np.pi / 4)
        right = mono * np.sin((self.__pan + 1) * np.pi / 4)
        return np.stack([left, right], axis=-1)

    def trigger(self, start_time=0):
        """Start playing the voice from the beginning."""
        self.__voice.reset_position()
        self.is_playing = True
        self.start_time = start_time  # Store start time

    def stop(self):
        """Stop playing the voice."""
        self.is_playing = False

    @property
    def channel_id(self):
        return self.__id

    @property
    def voice(self):
        return self.__voice

    @property
    def volume(self):
        return self.__volume

    @property
    def pan(self):
        return self.__pan

    @voice.setter
    def voice(self, value):
        self.__voice = value

    @volume.setter
    def volume(self, value):
        self.__volume = value

    @pan.setter
    def pan(self, value):
        self.__pan = value
