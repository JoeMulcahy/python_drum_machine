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

        self.__save_profile()

    def __save_profile(self):
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
            with shelve.open(shelve_path) as db:
                db['dictionary'] = self.__profile_dict
                QMessageBox.information(self, "Success", f"Profile saved as:\n{shelve_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        print(f'Debug: saved profile: \n-------------------------------------------\n')
        self.visualise_profile()

    def visualise_profile(self):
        if self.__profile_dict:
            for k, v in self.__profile_dict.items():
                print(f'{k} {v}')




