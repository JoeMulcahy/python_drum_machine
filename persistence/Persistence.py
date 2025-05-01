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

channels = []
patterns = {}
save_dict = {}


@staticmethod
def save_profile(settings):
    pass
    # settings in form of ['channel', 'patterns', 'playable_steps', 'time_resolution', 'transport']
