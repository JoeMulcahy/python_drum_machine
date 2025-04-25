import numpy as np

from sound_engine import Voice


class Channel:
    def __init__(self, channel_id, voice: Voice, volume=1.0, pan=0.0):
        self.__id = channel_id
        self.__voice = voice
        self.__volume = volume  # 0.0 to 1.0
        self.__pan = pan        # -1.0 (L) to 1.0 (R)

    def next_stereo_chunk(self, frames: int) -> np.ndarray:
        mono = self.__voice.next_chunk(frames) * self.__volume
        # Simple equal-power panning
        left = mono * np.cos((self.__pan + 1) * np.pi / 4)
        right = mono * np.sin((self.__pan + 1) * np.pi / 4)
        return np.stack([left, right], axis=-1)

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
