from songstransfer import *

"""def test_Transfer():
	#TODO transfer songs to a new destination folder
	#TODO remove a song from the destination folder
	#TODO transfer songs to the destination folder (with almost all existing songs) to check if the previous removed song was copied
	#TODO transfer playlists files
	#TODO remove the destination folder"""

# Save the ubication of the .xml archive with the iTunes library to export
librarylocation = "./Test/iTunes Music Library.xml"

# Save the ubication where the library want to import
archivefinallocation = "./destination"

# Original archive ubication
originalarchivelocation = "./Test/Music"

#songsTransferer(librarylocation, archivefinallocation, originalarchivelocation)

playlistTransferer(librarylocation, archivefinallocation)
