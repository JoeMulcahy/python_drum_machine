import numpy as np


class Voice:
    def __init__(self, data: np.ndarray, samplerate: int):
        self.data = data
        self.samplerate = samplerate
        self.position = 0  # Current playback index
        self.active = True

    def next_chunk(self, frames: int) -> np.ndarray:
        if not self.active or self.position >= len(self.data):
            self.active = False
            return np.zeros(frames, dtype=np.float32)

        end = self.position + frames
        chunk = self.data[self.position:end]
        self.position = end

        # Pad with zeros if end of audio
        if len(chunk) < frames:
            chunk = np.pad(chunk, (0, frames - len(chunk)))

        return chunk
