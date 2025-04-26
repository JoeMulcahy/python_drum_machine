import shelve
from random import choice


class PatternManager:
    def __init__(self, number_of_banks=4, number_of_global_patterns=9, number_of_channels=8, number_of_steps=16):
        self.__bank_index = 0
        self.__global_pattern_index = 0
        self.__channel_pattern_index = 0

        self.__number_of_steps = number_of_steps
        self.__number_of_channels = number_of_channels
        self.__number_of_global_patterns = number_of_global_patterns
        self.__number_of_banks = number_of_banks

        self.__bank_dict = dict()
        self.__global_pattern_list = list()
        self.__channel_pattern_list = list()
        self.initial_pattern = [0 for i in range(self.__number_of_steps)]

        for i in range(self.__number_of_channels):
            self.__channel_pattern_list.append(self.initial_pattern)

        for i in range(self.__number_of_global_patterns):
            self.__global_pattern_list.append(self.__channel_pattern_list)

        for i in range(self.__number_of_banks):
            self.__bank_dict[i] = self.__global_pattern_list

    @property
    def bank_dict(self):
        return self.__bank_dict

    @bank_dict.setter
    def bank_dict(self, value):
        self.__bank_dict = value

    def get_channel_pattern(self, i1, i2, i3):
        return self.__bank_dict[i1][i2][i3]

    def set_channel_pattern(self, i1, i2, i3, pattern):
        self.__bank_dict[i1][i2][i3] = pattern

    def get_global_pattern(self, index):
        return self.__global_pattern_list[index]

    def load_banks(self, filename):
        with shelve.open(filename) as shelve_file:
            self.__bank_dict = shelve_file

    def save_banks(self, filename):
        with shelve.open(filename) as shelve_file:
            shelve_file = self.__bank_dict

    @staticmethod
    def generate_random_pattern(pattern_length=16):
        return [choice([0, 1]) for i in range(pattern_length)]

    @staticmethod
    def generate_random_global_pattern(number_of_channel=8, pattern_length=16):
        patterns = []
        for i in range(number_of_channel):
            patterns.append(PatternManager.generate_random_pattern(pattern_length))

        return patterns

    @staticmethod
    def generate_global_patterns_for_select(number_of_global_patterns=8, number_of_channel=8, pattern_length=16):
        global_patterns = []
        for i in range(number_of_global_patterns):
            global_patterns.append(PatternManager.generate_random_global_pattern(number_of_channel, pattern_length))

        return global_patterns

    @staticmethod
    def generate_random_banks(number_of_banks=4, number_of_global_patterns=8, number_of_channels=8, pattern_length=16):
        banks = dict()
        for i in range(number_of_banks):
            banks[i] = PatternManager.generate_global_patterns_for_select(
                number_of_global_patterns, number_of_channels,pattern_length)

        return banks

    @staticmethod
    def shift_pattern_left(pattern, *, amount=1):
        shifted = []
        for i in range(len(pattern)):
            shifted.append(pattern[(i - amount) % len(pattern)])

        return shifted

    @staticmethod
    def shift_pattern_right(pattern, *, amount=1):
        shifted = []
        for i in range(len(pattern)):
            shifted.append(pattern[(i + amount) % len(pattern)])

        return shifted

    @staticmethod
    def generate_sequenced_pattern(pattern_length, every_x_steps):
        pattern = []
        for i in range(pattern_length):
            if i % every_x_steps == 0:
                pattern.append(1)
            else:
                pattern.append(0)

        return pattern
