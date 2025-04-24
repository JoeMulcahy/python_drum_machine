import numpy as np

from sound_engine import Voice


class Channel:
    def __init__(self, voice: Voice, volume=1.0, pan=0.0):
        self.voice = voice
        self.volume = volume  # 0.0 to 1.0
        self.pan = pan        # -1.0 (L) to 1.0 (R)

    def next_stereo_chunk(self, frames: int) -> np.ndarray:
        mono = self.voice.next_chunk(frames) * self.volume
        # Simple equal-power panning
        left = mono * np.cos((self.pan + 1) * np.pi / 4)
        right = mono * np.sin((self.pan + 1) * np.pi / 4)
        return np.stack([left, right], axis=-1)
