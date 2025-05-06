"""
Persistence

allows for the loading and saving of application profiles
saved values include:
    -   channel settings
        -   channel name
        -   selected sound file
        -   dial values

    -   patterns
        -   pattern dictionary

    -   playable steps
    -   timing resolution

    -   transport
        -   bpm


"""
import os
import shelve

from PyQt6.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QWidget

import settings


class Profile(QWidget):
    def __init__(self,
                 channel_settings, mute_list, solo_list,
                 beats_per_minute, beats_per_bar, meter, metronome_on, pattern_dict,
                 pattern_bank, pattern_selected, playable_steps, time_resolution,
                 timing_flam, timing_swing, timing_humanise, timing_humanise_strength
                 ):

        super().__init__()

        self.__profile_dict = dict()
        self.__profile_name = ""
        self.__profile_dict['profile_name'] = ""
        self.__profile_dict['channel_settings'] = channel_settings
        self.__profile_dict['mute_list'] = mute_list
        self.__profile_dict['solo_list'] = solo_list
        self.__profile_dict['beats_per_minute'] = beats_per_minute
        self.__profile_dict['beats_per_bar'] = beats_per_bar
        self.__profile_dict['meter'] = meter
        self.__profile_dict['metronome_on'] = metronome_on
        self.__profile_dict['pattern_dict'] = pattern_dict
        self.__profile_dict['pattern_bank'] = pattern_bank
        self.__profile_dict['pattern_selected'] = pattern_selected
        self.__profile_dict['playable_steps'] = playable_steps
        self.__profile_dict['time_resolution'] = time_resolution
        self.__profile_dict['timing_flam'] = timing_flam
        self.__profile_dict['timing_swing'] = timing_swing
        self.__profile_dict['timing_humanise'] = timing_humanise
        self.__profile_dict['timing_humanise_strength'] = timing_humanise_strength

    def save_profile(self):
        path = settings.PROFILE_DIRECTORY
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", path)
        if not directory:
            return

        filename, ok = QInputDialog.getText(self, "Profile", "Enter Profile name:")
        if not ok or not filename.strip():
            return

        self.__profile_dict['profile_name'] = filename
        self.__profile_name = filename
        filename = filename.strip().replace(' ', '_')
        shelve_path = os.path.join(directory, filename)

        try:
            with shelve.open(shelve_path) as profile:
                profile['dictionary'] = self.__profile_dict
                QMessageBox.information(self, "Success", f"Profile saved as:\n{shelve_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_profile(self):
        path = settings.PROFILE_DIRECTORY
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            path,
            "Python Files (*.dat)"  # Filter
        )

        shelve_path = os.path.splitext(file_path)[0]

        if not file_path:
            return

        if file_path:
            print(f'file path: {shelve_path}')
            try:
                with shelve.open(shelve_path) as profile:
                    self.__profile_dict = profile['dictionary']
                    return self.__profile_dict
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")

    def visualise_profile(self):
        if self.__profile_dict:
            for k, v in self.__profile_dict.items():
                print(f'{k} {v}')

    @property
    def profile_name(self):
        return self.__profile_dict['profile_name']

    @property
    def channel_settings(self):
        return self.__profile_dict['channel_settings']

    @property
    def mute_list(self):
        return self.__profile_dict['mute_list']

    @property
    def solo_list(self):
        return self.__profile_dict['solo_list']

    @property
    def beats_per_minute(self):
        return self.__profile_dict['beats_per_minute']

    @property
    def beats_per_bar(self):
        return self.__profile_dict['beats_per_bar']

    @property
    def meter(self):
        return self.__profile_dict['meter']

    @property
    def metronome_on(self):
        return self.__profile_dict['metronome_on']

    @property
    def pattern_dictionary(self):
        return self.__profile_dict['pattern_dict']

    @property
    def pattern_bank_index(self):
        return self.__profile_dict['pattern_bank']

    @property
    def selected_pattern_index(self):
        return self.__profile_dict['pattern_selected']

    @property
    def playable_steps(self):
        return self.__profile_dict['playable_steps']

    @property
    def time_resolution_index(self):
        return self.__profile_dict['time_resolution']

    @property
    def flam_time(self):
        return self.__profile_dict['timing_flam']

    @property
    def swing_time(self):
        return self.__profile_dict['timing_swing']

    @property
    def humanise_time(self):
        return self.__profile_dict['timing_humanise']

    @property
    def humanise_strength(self):
        return self.__profile_dict['timing_humanise_strength']








