from enum import Enum


class SoundType(Enum):
    SOUND_WAVE = 1,
    SOUND_SAMPLE = 2


class WaveForm(Enum):
    SIN = 1,
    SQUARE = 2,
    TRIANGLE = 3
