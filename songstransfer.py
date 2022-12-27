from musiclibrary import *
from os.path import exists
from shutil import copy

# Save the ubication of the .xml archive with the iTunes library to export
libraryubication = input

# Save the ubication where the library want to import
archivefinalubication = input

# Original archive ubication
originalarchiveubication = input

# iTunes library to export
library = Library(libraryubication)


for songs in library.songs:
    # Create a trucknumber with 2 figures
    trucknumber = str(songs.trucknumber)
    if len(str(songs.trucknumber)) == 0:
        trucknumber = "0"+str(songs.trucknumber)

    # Corrovorate if the .mp3 archive exist in the final file, if not copy the archive
    if exists(archivefinalubication+"/"+songs.artist+"/"+songs.album+""+trucknumber+songs.title+".mp3") == False:
        copy(originalarchiveubication, archivefinalubication+"/"+songs.artist +
             "/"+songs.album+"/"+trucknumber+songs.title+".mp3")
