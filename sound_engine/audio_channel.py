import numpy as np

from sound_engine.audio_filters.simple_equalisation import SimpleEqualisation


class AudioChannel:
    def __init__(self, channel_id, sample, volume=1.0, pan_scaled=0.0):
        self.__id = channel_id
        self.__voice = sample
        self.__volume = volume  # 0.0 to 1.0
        self.__pan = 0  # -1.0 (L) to 1.0 (R)
        self.__pan_scaled = pan_scaled  # 0.0 to 1.0
        self.is_playing = False  # Add is_playing attribute
        self.start_time = 0  # Add start_time attribute

        self.__hsf_gain = 0.0  # High shelf gain in dB
        self.__hsf_frequency = 2000.0  # High shelf cutoff frequency

        self.__parametric_gain_1 = 0.0  # parametric eq gain
        self.__parametric_q_1 = 0.707  # parametric q value
        self.__parametric_frequency_1 = 500  # parametric eq frequency

        self.__parametric_gain_2 = 0.0  # parametric eq gain
        self.__parametric_q_2 = 0.707  # parametric q value
        self.__parametric_frequency_2 = 2000  # parametric eq frequency

        self.__parametric_gain_3 = 0.0  # parametric eq gain
        self.__parametric_q_3 = 0.707  # parametric q value
        self.__parametric_frequency_3 = 5000  # parametric eq frequency

        self.__lsf_gain = 0.0  # Low shelf gain in dB
        self.__lsf_frequency = 100.0  # Low shelf cutoff frequency

        self.__is_muted = False

    def next_stereo_chunk(self, frames: int) -> np.ndarray:
        if not self.is_playing or self.__is_muted:
            return np.zeros((frames, 2), dtype=np.float32)

        mono = self.__voice.next_chunk(frames) * self.__volume

        if mono.ndim > 1:
            mono = mono.squeeze(axis=1)
            mono = self.apply_equalisation(mono)

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

    def apply_equalisation(self, data=None):
        """Apply proper high and low shelving filters."""
        if data is None:
            return None

        if self.__lsf_gain != 0:
            data = SimpleEqualisation.apply_eq(
                data=data,
                gain_db=self.__lsf_gain,
                frequency=self.__lsf_frequency,
                eq_type='low_shelf'
            )

        if self.__hsf_gain != 0:
            data = SimpleEqualisation.apply_eq(
                data=data,
                gain_db=self.__hsf_gain,
                frequency=self.__hsf_frequency,
                eq_type='high_shelf'
            )

        if self.__parametric_gain_1 != 0:
            data = SimpleEqualisation.apply_eq(
                data=data,
                gain_db=self.__parametric_gain_1,
                frequency=self.__parametric_frequency_1,
                q=self.__parametric_q_1,
                eq_type='parametric'
            )

        if self.__parametric_gain_2 != 0:
            data = SimpleEqualisation.apply_eq(
                data=data,
                gain_db=self.__parametric_gain_2,
                frequency=self.__parametric_frequency_2,
                q=self.__parametric_q_2,
                eq_type='parametric'
            )

        if self.__parametric_gain_3 != 0:
            data = SimpleEqualisation.apply_eq(
                data=data,
                gain_db=self.__parametric_gain_3,
                frequency=self.__parametric_frequency_3,
                q=self.__parametric_q_3,
                eq_type='parametric'
            )

        return data

    ##########################################################################
    ##########################################################################
    ##  setters and getters
    ##########################################################################
    ##########################################################################

    """     
        high shelf eq       
    """

    @property
    def high_shelf_eq_gain(self):
        return self.__hsf_gain

    @high_shelf_eq_gain.setter
    def high_shelf_eq_gain(self, value):
        # value is between 0 and 100 from gui dial
        self.__hsf_gain = (value - 50) * 0.3  # scale 15db to +15db

    @property
    def high_shelf_eq_frequency(self):
        return self.__hsf_frequency

    @high_shelf_eq_frequency.setter
    def high_shelf_eq_frequency(self, value):
        self.__hsf_frequency = value

    """     
        low shelf eq       
    """

    @property
    def low_shelf_eq_gain(self):
        return self.__lsf_gain

    @low_shelf_eq_gain.setter
    def low_shelf_eq_gain(self, value):
        # value is between 0 and 100 from gui dial
        self.__lsf_gain = (value - 50) * 0.3  # scale 15db to +15db

    @property
    def low_shelf_eq_frequency(self):
        return self.__lsf_frequency

    @low_shelf_eq_frequency.setter
    def low_shelf_eq_frequency(self, value):
        self.__lsf_frequency = value

    """     
        parametric eq 1      
    """

    @property
    def parametric_eq_gain_1(self):
        return self.__parametric_gain_1

    @parametric_eq_gain_1.setter
    def parametric_eq_gain_1(self, value):
        self.__parametric_gain_1 = (value - 50) * 0.3  # scale 15db to +15db

    @property
    def parametric_q_1(self):
        return self.__parametric_q_1

    @parametric_q_1.setter
    def parametric_q_1(self, value):
        self.__parametric_q_1 = value

    @property
    def parametric_frequency_1(self):
        return self.__parametric_frequency_1

    @parametric_frequency_1.setter
    def parametric_frequency_1(self, value):
        self.__parametric_frequency_1 = value

    """     
        parametric eq 2     
    """

    @property
    def parametric_eq_gain_2(self):
        return self.__parametric_gain_2

    @parametric_eq_gain_2.setter
    def parametric_eq_gain_2(self, value):
        self.__parametric_gain_2 = (value - 50) * 0.3  # scale 15db to +15db

    @property
    def parametric_q_2(self):
        return self.__parametric_q_2

    @parametric_q_2.setter
    def parametric_q_2(self, value):
        self.__parametric_q_2 = value

    @property
    def parametric_frequency_2(self):
        return self.__parametric_frequency_2

    @parametric_frequency_2.setter
    def parametric_frequency_2(self, value):
        self.__parametric_frequency_2 = value

    """     
        parametric eq 3      
    """

    @property
    def parametric_eq_gain_3(self):
        return self.__parametric_gain_3

    @parametric_eq_gain_3.setter
    def parametric_eq_gain_3(self, value):
        self.__parametric_gain_3 = (value - 50) * 0.3  # scale 15db to +15db

    @property
    def parametric_q_3(self):
        return self.__parametric_q_3

    @parametric_q_3.setter
    def parametric_q_3(self, value):
        self.__parametric_q_3 = value

    @property
    def parametric_frequency_3(self):
        return self.__parametric_frequency_3

    @parametric_frequency_3.setter
    def parametric_frequency_3(self, value):
        self.__parametric_frequency_3 = value

    """     
        channel id     
    """

    @property
    def channel_id(self):
        return self.__id

    """     
        voice     
    """

    @property
    def voice(self):
        return self.__voice

    @voice.setter
    def voice(self, value):
        self.__voice = value

    """     
         volume    
    """

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = value

    """     
         pan     
    """

    @property
    def pan_scaled(self):
        return self.__pan_scaled

    @pan_scaled.setter
    def pan_scaled(self, value):
        self.__pan_scaled = value
        self.__pan = (self.__pan_scaled - 0.5) * 2

    """     
        is_muted  
    """
    @property
    def is_muted(self):
        return self.__is_muted

    @is_muted.setter
    def is_muted(self, value):
        self.__is_muted = value
