# Directories
from PyQt6.QtWidgets import QSizePolicy

ROOT_DIRECTORY = "C:\\Users\\josep\\Desktop\\Python Programming"
PROFILE_DIRECTORY = "C:\\Users\\josep\\Desktop\\Python Programming\\Step Seq\\profiles"
IMAGES_DIRECTORY = "C:\\Users\\josep\\Desktop\\Python Programming\\Step Seq\\images"

# Styling

FIXED_SIZE_POLICY = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
EXPAND_SIZE_POLICY = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
HORIZONTAL_STRETCH_POLICY = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
VERTICAL_STRETCH_POLICY = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

# Module styling - styling common to all modules
LABEL_STYLE_1 = """
QLabel { 
    font-size: 12px; 
    font-weight: bold
    }
"""

LABEL_STYLE_2 = """
QLabel { 
    font-size: 8px; 
    font-weight: bold}
    }
"""

BUTTON_STYLE_1 = """
QPushButton {
    font-size: 9px;  
    font-weight: bold; 
    background-color: #3d282c; 
    color: white;
    }
"""

BUTTON_STYLE_2 = """
QPushButton {
    font-size: 9px;  
    font-weight: bold; 
    background-color: #172e1d;
    color: white;
    }
"""

GROUPBOX_STYLE_1 = """
    QGroupBox {
        font-weight: bold;
        border: 2px solid gray;
        border-radius: 3px;
        margin-top: 1ex; 
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
"""

GROUPBOX_STYLE_2 = """
QGroupBox { 
    background-color: #23224a; 
    border: 1px solid gray;
    }
"""

GROUPBOX_STYLE_3 = """
QGroupBox { 
    background-color: #23224a; 
    border: 1px solid gray;
    }
"""

CHECKBOX_STYLE_1 = """
QCheckBox {
    border: 1px solid gray;
}
"""

# Drum Machine Channel Styling
CHANNEL_DEFAULT_STYLE = """ 
QGroupBox { 
    background-color: #23224a; 
    border: 1px solid gray;
    }
"""
CHANNEL_SELECT_STYLE = """ 
QGroupBox { 
    background-color: #413f75; 
    border: 1px solid gray;
    }
"""

RESET_BUTTON_STYLE = """
QPushButton {
    font-size: 9px;  
    font-weight: bold; 
    background-color: #c41431; 
    color: white;
    }
"""
SOLO_BUTTON_ON_STYLE = """
QPushButton {
    font-size: 9px;  
    font-weight: bold; 
    background-color: #14c443; 
    color: white;
    }
"""
MUTE_BUTTON_ON_STYLE = """
QPushButton {
    font-size: 9px;  
    font-weight: bold; 
    background-color: #bbc414; 
    color: white;}
"""

CHANNEL_NUMBER_OFF_STYLE = """
QLabel { 
    font-size: 16px; 
    font-weight: bold; 
    color: #aaaaaa; 
    }
"""
CHANNEL_NUMBER_ON_STYLE = """
QLabel { 
    font-size: 16px; 
    font-weight: bold; 
    color: #cc2216; 
    }
"""

# Tempo module styling
TEMPO_SPINBOX_STYLE = """
QSpinBox {
    font-size: 24px;       
    color: #ff5733;        
    }
"""

# Metronome module styling
BEATS_PER_BAR_SPINBOX_STYLING = """
QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
    width: 0;
    height: 0;
    border: none;
    }
"""

BEAT_TYPE_SPINBOX_STYLING = """
QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
    width: 0;
    height: 0;
    border: none;
    }
"""

# Pattern Select Module styling
PATTERN_BUTTON_DEFAULT_STYLING = """
QPushButton { 
    background-color: #3498db; 
    color: white; 
    }
"""

PATTERN_BUTTON_ON_STYLING = """
QPushButton { 
    font-weight: 900;
    background-color: #7373d1;
    color: white; 
    }
"""

BANK_BUTTON_DEFAULT_STYLING = """
QPushButton { 
    background-color: #6698db;
    color: white; 
    }
"""

BANK_BUTTON_ON_STYLING = """
QPushButton { 
    font-weight: 900;
    background-color: #ff99ef;
    color: white; 
    }
"""

# Stepper Module Styling
STEPPER_BUTTON_DEFAULT_STYLING = """
QPushButton { 
    background-color: #3498db; 
    color: white; 
    }
"""

STEPPER_BUTTON_ON_STYLING = """
QPushButton { 
    background-color: #ef9912; 
    color: white; 
    }
"""

STEPPER_BUTTON_PLAY_STYLING = """
QPushButton { 
    background-color: #12ff12; 
    color: white; 
    }
"""

STEPPER_INDICATOR_DEFAULT_STYLING = """
QLabel {
    font-size: 40px; 
    color: #12ff12;
    }
"""

STEPPER_INDICATOR_ON_STYLING = """
QLabel {
    font-size: 40px; 
    color: #ff1212;
    }
"""

STEPPER_INDICATOR_ALTERNATIVE_STYLING = """
QLabel {
    font-size: 40px; 
    color: #ffff12;
    }
"""

STEP_FREQUENCY_SPINBOX_STYLING = """
QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
    width: 0;
    height: 0;
    border: none;
    }
"""






