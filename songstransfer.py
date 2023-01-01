from musiclibrary import *
from os.path import exists, join
from os import makedirs, remove, listdir
from shutil import copy2 as copy
from re import sub
from io import open

# Special characters
specialcharacters = r"\/|\\|&|\?|!|\*|@|\$|€|%|=|~|\[|\]|{|}|<|>|\^|´|’|\.$"
specialcharacterstitle = r"\/|\\|&|\?|!|\*|@|\$|€|%|=|~|\[|\]|{|}|<|>|\^|´|’"

# Synchronize origin and destination folder


def songsTransferer(librarylocation, filefinallocation, originalfilelocation):

    # iTunes library to export
    library = Library(librarylocation)

    for songs in library.songs:

        # artist without special characters
        artist = sub(specialcharacters, "_", songs.artist)
        # title without special characters
        title = sub(specialcharacterstitle, "_", songs.title)
        # album without special characters
        album = sub(specialcharacters, "_", songs.album)

        # Create a trucknumber with 2 figures
        tracknumber = ""
        if songs.tracknumber < 10:
            tracknumber += "0"
        tracknumber += str(songs.tracknumber)

        # create the folder tree
        folder = "/" + artist + "/" + album

        # create the file path
        file = "/" + folder + "/"
        if songs.discnumber is not None:
            file += str(songs.discnumber)+"-"
        file += tracknumber+" "+title+".mp3"

        # Corrovorate if the .mp3 archive exist in the final file, if not copy the archive
        if exists(filefinallocation+file) == False:
            if exists(filefinallocation+folder) == False:
                makedirs(filefinallocation+folder)
                copy(originalfilelocation+file, filefinallocation+file)
            else:
                copy(originalfilelocation+file, filefinallocation+file)

# Export playlist from origin to final folder


def playlistTransferer(librarylocation, archivefinallocation):

    # list of all archive with .m3u extention in final folder
    listplaylist = listdir(archivefinallocation)

    # remove all prexistiing files with .m3u extention in final folder
    for item in listplaylist:
        if item.endswith(".m3u"):
            remove(join(archivefinallocation, item))

    # iTunes Library to export
    library = Library(librarylocation)

    for songs in library.songs:

        # artist without special characters
        artist = sub(specialcharacters, "_", songs.artist)
        # title without special characters
        title = sub(specialcharacterstitle, "_", songs.title)
        # album without special characters
        album = sub(specialcharacters, "_", songs.album)

        # Create a trucknumber with 2 figures
        tracknumber = ""
        if songs.tracknumber < 10:
            tracknumber += "0"
        tracknumber += str(songs.tracknumber)

        # create the folder tree
        folder = "/" + artist + "/" + album

        # create the file path
        file = "/" + folder + "/"
        if songs.discnumber is not None:
            file += str(songs.discnumber)+"-"
        file += tracknumber+" "+title+".mp3"

        # name of song playlist
        nameplaylist = ""

        # cover all the song pllaylists
        for x in library.playlists:
            index = 0
            while index <= x.getLength()-1:
                if x.getSongs()[index].id == songs.id:
                    nameplaylist = x.name
                index += 1

            # enter in this condiction if song belong to a playlist
            if nameplaylist != None:

                # create a .m3u file if it doesn't exist and add the song's path to this file
                if exists(archivefinallocation + "/" + nameplaylist + ".m3u") == False:
                    newplaylist = open(archivefinallocation + "/" +
                                       nameplaylist + ".m3u", "a")
                    newplaylist.write(archivefinallocation + file + "\n")
                    newplaylist.close()
                    nameplaylist = ""

                # add the song's path to the playlist file if it's exist
                else:
                    newplaylist = open(archivefinallocation + "/" +
                                       nameplaylist + ".m3u", "a")
                    newplaylist.write(archivefinallocation + file + "\n")
                    newplaylist.close()
                    nameplaylist = ""
