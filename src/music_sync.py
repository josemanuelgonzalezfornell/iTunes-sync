from src.music_library import *
from os.path import exists, join
from os import makedirs, remove, listdir
from shutil import copy2 as copy
from re import sub
from io import open

# Files
SEPARATOR = "/"
SONG_EXTENSION = ".mp3"
PLAYLIST_EXTENSION = ".m3u"
# Special characters
SPECIAL_CHARACTERS = r"\/|\\|&|\?|!|\*|@|\$|€|%|=|~|\[|\]|{|}|<|>|\^|´|’"
SPECIAL_CHARACTERS_FOLDER = SPECIAL_CHARACTERS + "|\.$"


def sync_songs(library_path: str, source_path: str, destination_path: str) -> None:
    """It syncs the destination folder to contains the songs files according to the source music library.

    Args:
            library_path (str): Absolute file path to the source music library XML file.
            source_path (str): Absolute folder path to the source music folder.
            destination_path (str): Absolute folder path to the destination music folder.
    """
    # iTunes library to export
    library = Library(library_path)
    for song in library.songs:
        # Folder relative path
        folder = get_folder_path(song)
        # File relative path
        file = get_file_path(song)
        # Check if the song file exists in the destination folder. If not, copy the song file.
        if not exists(destination_path + SEPARATOR + file):
            if not exists(destination_path + SEPARATOR + folder):
                makedirs(destination_path + SEPARATOR + folder)
                copy(source_path + SEPARATOR +
                     file, destination_path + SEPARATOR + file)
            else:
                copy(source_path + SEPARATOR +
                     file, destination_path + SEPARATOR + file)
    for artist in listdir(destination_path):
        for album in listdir(artist):
            for song in listdir(album):
                # Folder relative path
                folder = get_folder_path(song)
                # File relative path
                file = get_file_path(song)
                # Check if the song file exists in the destination folder. If not, copy the song file.
                if not exists(source_path + SEPARATOR +
                              folder):
                    remove(destination_path + SEPARATOR +
                           folder)
                elif not exists(source_path + SEPARATOR + file):
                    remove(destination_path + SEPARATOR + file)


def sync_playlists(library_path: str, destination_path: str) -> None:
    """It updates the playlists in the destination folder according to the source music library.

    Args:
            library_path (str): Absolute file path to the source music library XML file.
            destination_path (str): Absolute folder path to the destination music folder.
    """
    # Remove all prexisting playlists files from the destination folder
    for item in listdir(destination_path):
        if item.endswith(PLAYLIST_EXTENSION):
            remove(join(destination_path, item))
        # FIXME it does not work. See test_sync_playlists.
    # Source music library
    library = Library(library_path)
    # Create playlists files
    for playlist in library.playlists:
        for song in playlist.get_songs():
            # Artist without special characters
            song_file = get_file_path(song)
            # Create a playlist file only if it doesn't exist and add the song path to this file
            if not exists(destination_path + SEPARATOR + playlist.name + PLAYLIST_EXTENSION):
                playlist_file = open(destination_path + SEPARATOR +
                                     playlist.name + PLAYLIST_EXTENSION, "w")
                playlist_file.write(song_file + "\n")
                playlist_file.close()

            # Add the song path to the playlist file only if it exists
            else:
                playlist_file = open(destination_path + SEPARATOR +
                                     playlist.name + PLAYLIST_EXTENSION, "a")
                playlist_file.write(song_file + "\n")
                playlist_file.close()


def get_folder_path(song: Song) -> str:
    """It gets the relative path of the song folder according to its metadata.

    Args:
                    song (Song): Object of Song class containing all metadata.

    Returns:
                    str: Path name to the song folder, relative to the music folder.
    """
    # Artist without special characters
    artist = sub(SPECIAL_CHARACTERS_FOLDER + "|\.$", "_", song.artist)
    # Album without special characters
    album = sub(SPECIAL_CHARACTERS_FOLDER + "|\.$", "_", song.album)
    # Create the folder path
    path = artist + SEPARATOR + album
    return path


def get_file_path(song: Song) -> str:
    """It gets the relative path of the song file according to its metadata.

    Args:
            song (Song): object of Song class containing all metadata.

    Returns:
            str: path name to the song file, relative to the music folder.
    """
    # Title without special characters
    title = sub(SPECIAL_CHARACTERS, "_", song.title)
    # Track number with two digits
    track_number = ""
    if song.track_number < 10:
        track_number += "0"
    track_number += str(song.track_number)
    # Create the file path
    path = get_folder_path(song) + SEPARATOR
    if song.disc_number is not None:
        path += str(song.disc_number) + "-"
    path += track_number + " " + title + SONG_EXTENSION
    return path
