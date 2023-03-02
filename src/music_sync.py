from src.music_library import *
from re import sub
from io import open
from os.path import exists, join
from os import makedirs as create_dir
from os import remove
from os import listdir as dir
from shutil import copy2 as copy
from shutil import rmtree as remove_tree

# Files
SEPARATOR = '/'
SONG_EXTENSION = '.mp3'
PLAYLIST_EXTENSION = '.m3u'
# Special characters
SPECIAL_CHARACTERS = r'\/|\\|&|\?|!|\*|@|\$|€|%|=|~|\[|\]|{|}|<|>|\^|´|’'
SPECIAL_CHARACTERS_FOLDER = SPECIAL_CHARACTERS + '|\.$'


def sync_library(library_path: str, source_path: str, destination_path: str) -> None:
    """It syncs the the destination folder to contains the songs and playlists according to the source music library.

    Args:
        library_path (str): Absolute file path to the source music library XML file.
        source_path (str): Absolute folder path to the source music folder.
        destination_path (str): Absolute folder path to the destination music folder.
    """
    # iTunes library to export
    library = Library(library_path)
    sync_songs(library, source_path, destination_path)
    sync_playlists(library, destination_path)


def sync_songs(library: Library, source_path: str, destination_path: str) -> None:
    """It syncs the destination folder to contains the songs files according to the source music library.

    Args:
        library (Library): Object of Library class.
        source_path (str): Absolute folder path to the source music folder.
        destination_path (str): Absolute folder path to the destination music folder.
    """
    artists = set()  # Set of folder paths to library artists
    albums = set()  # Set of folder paths to library albums
    songs = set()  # Set of file paths to library songs
    for song in library.songs:
        # Folder relative path
        folder = get_folder_path(song)
        # File relative path
        file = get_file_path(song)
        # Library folders
        artists.add(replace_path_characters(song.artist))
        albums.add(folder)
        songs.add(file)
        # Check if the song file exists in the destination folder. If not, copy the song file.
        if not exists(destination_path + SEPARATOR + file):
            if not exists(destination_path + SEPARATOR + folder):
                create_dir(destination_path + SEPARATOR + folder)
                copy(source_path + SEPARATOR +
                     file, destination_path + SEPARATOR + file)
            else:
                copy(source_path + SEPARATOR +
                     file, destination_path + SEPARATOR + file)
    # Destination clean
    for artist in dir(destination_path):
        if not artist in artists:
            remove_tree(destination_path + SEPARATOR +
                        artist, ignore_errors=True)
        else:
            for album in dir(destination_path + SEPARATOR + artist):
                album_path = artist + SEPARATOR + album
                if not album_path in albums:
                    remove_tree(destination_path + SEPARATOR +
                                album_path, ignore_errors=True)
                else:
                    for song in dir(destination_path + SEPARATOR + album_path):
                        song_path = album_path + SEPARATOR + song
                        if not song_path in songs:
                            remove(destination_path + SEPARATOR + song_path)


def sync_playlists(library: Library, destination_path: str) -> None:
    """It updates the playlists in the destination folder according to the source music library.

    Args:
        library (Library): Object of Library class.
        destination_path (str): Absolute folder path to the destination music folder.
    """
    # Remove all prexisting playlists files from the destination folder
    if exists(destination_path):
        for playlist in dir(destination_path):
            if playlist.endswith(PLAYLIST_EXTENSION):
                remove(join(destination_path, playlist))
    else:
        create_dir(destination_path)
    # Create playlists files
    for playlist in library.playlists:
        for song in playlist.get_songs():
            # Artist without special characters
            song_file = get_file_path(song)
            # Create a playlist file only if it doesn't exist and add the song path to this file
            if exists(destination_path + SEPARATOR + playlist.name + PLAYLIST_EXTENSION):
                mode = 'a'  # Editing mode
            else:
                mode = 'w'  # Creation mode
            playlist_file = open(
                destination_path + SEPARATOR + playlist.name + PLAYLIST_EXTENSION, mode)
            playlist_file.write(song_file + '\n')
            playlist_file.close()


def replace_path_characters(directory: str) -> str:
    """It replace special characters with character _ for using in path strings.

    Args:
        directory (str): String to be replaced.

    Returns:
        str: replaced string.
    """
    return sub(SPECIAL_CHARACTERS_FOLDER + '|\.$', '_', directory)


def get_folder_path(song: Song) -> str:
    """It gets the relative path of the song folder according to its metadata.

    Args:
        song (Song): Object of Song class containing all metadata.

    Returns:
        str: Path name to the song folder, relative to the music folder.
    """
    # Artist without special characters
    artist = replace_path_characters(song.artist)
    # Album without special characters
    album = replace_path_characters(song.album)
    # Create the folder path
    path = artist + SEPARATOR + album
    return path


def get_file_path(song: Song) -> str:
    """It gets the relative path of the song file according to its metadata.

    Args:
        song (Song): Object of Song class containing all metadata.

    Returns:
        str: Path name to the song file, relative to the music folder.
    """
    # Title without special characters
    title = sub(SPECIAL_CHARACTERS, '_', song.title)
    # Track number with two digits
    track_number = ''
    if song.track_number < 10:
        track_number += '0'
    track_number += str(song.track_number)
    # Create the file path
    path = get_folder_path(song) + SEPARATOR
    if song.disc_number is not None:
        path += str(song.disc_number) + '-'
    path += track_number + ' ' + title + SONG_EXTENSION
    return path
