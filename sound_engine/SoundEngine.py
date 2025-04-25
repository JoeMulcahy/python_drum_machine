import numpy as np
import sounddevice as sd
import soundfile as sf
import threading

from sound_engine import AudioChannel


class SoundEngine:
    def __init__(self, samplerate=44100):
        self.channels = []
        self.samplerate = samplerate
        self.stream = sd.OutputStream(
            samplerate=samplerate,
            channels=2,
            dtype='float32',
            callback=self.audio_callback
        )
        self.lock = threading.Lock()

    def audio_callback(self, outdata, frames, time, status):
        with self.lock:
            mix = np.zeros((frames, 2), dtype=np.float32)
            for channel in self.channels:
                if channel.voice.active:
                    mix += channel.next_stereo_chunk(frames)
            # Clip to avoid overflow
            np.clip(mix, -1.0, 1.0, out=outdata)

    def add_channel(self, channel: AudioChannel):
        with self.lock:
            self.channels.append(channel)

    def play(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
