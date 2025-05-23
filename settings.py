# Directories
from PyQt6.QtWidgets import QSizePolicy

ROOT_DIRECTORY = "C:\\Users\\josep\\Desktop"
PROFILE_DIRECTORY = "C:\\Users\\josep\\Desktop\\Step Seq\\profiles"
IMAGES_DIRECTORY = "C:\\Users\\josep\\Desktop\\Step Seq\\images"

# Styling

FIXED_SIZE_POLICY = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
EXPAND_SIZE_POLICY = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
HORIZONTAL_STRETCH_POLICY = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
VERTICAL_STRETCH_POLICY = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

# Module styling - styling common to all modules
TEXT_STYLE_1 = """
QLabel { 
    font-size: 12px; 
    font-weight: bold
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
DEFAULT_BUTTON_STYLE = """
QPushButton {
    font-size: 9px;  
    font-weight: bold; 
    background-color: #2e2726; 
    color: white;
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

