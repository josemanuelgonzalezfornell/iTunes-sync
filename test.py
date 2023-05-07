# Libraries and constant variables used in tests. You need to add the following sentence to test python files:
# from test import *

import os
from src.music_library import *
from src.music_sync import *

TEST = os.path.dirname(os.path.realpath(__file__)) + SEPARATOR + "Test"
SOURCE = TEST + SEPARATOR + "source"
DESTINATION = TEST + SEPARATOR + "destination"
LIBRARIES = {
    "iTunes": [TEST + SEPARATOR + "iTunes Music Library.xml"],
    "Rhythmbox": [
        TEST + SEPARATOR + "rhythmdb.xml",
        TEST + SEPARATOR + "playlists.xml",
    ],
}
