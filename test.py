# Libraries and constant variables used in tests. You need to add the following sentence to test python files:
# from test import *

import os
from src.music_library import *
from src.music_sync import *

TEST = os.path.dirname(os.path.realpath(__file__)) + SEPARATOR + 'Test'
LIBRARY = TEST + SEPARATOR + 'iTunes Music Library.xml'
SOURCE = TEST + SEPARATOR + 'source'
DESTINATION = TEST + SEPARATOR + 'destination'
