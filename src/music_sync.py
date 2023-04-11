from src.music_library import *
from re import sub
from io import open
from os.path import exists, join
from os import makedirs as create_dir
from os import remove
from os import listdir as dir
from shutil import copy2 as copy
from shutil import rmtree as remove_tree
from tkinter import ttk

# Files
SEPARATOR = "/"
EXTENSION = ".m3u"
# Special characters
SPECIAL_CHARACTERS = r'\/|\\|\?|\*|@|\$|€|=|:|~|\[|\]|{|}|<|>|\^|"|´|’'


class Sync:
    """Class to sync the library."""

    library: Library = None  # Source music library XML file.
    source_path: str = None  # Absolute folder path to the source music folder.
    # Absolute folder path to the destination music folder.
    destination_path: str = None
    window: set = None  # Graphical user interface object.
    errors: set = []  # Songs and playlists that could not be synced.

    def __init__(
        self,
        library_path: str,
        source_path: str,
        destination_path: str,
        window: set = None,
    ) -> None:
        """It creates a sync process.

        Args:
            library_path (str): Absolute file path to the source music library XML file.
            source_path (str): Absolute folder path to the source music folder.
            destination_path (str): Absolute folder path to the destination music folder.
            window (set, optional): Graphical user interface object.
        """
        self.library = Library(library_path)
        self.source_path = source_path
        self.destination_path = destination_path
        self.window = window
        print(
            "Sync process created:\n- Library = "
            + self.library.file_name
            + "\n- Source = "
            + self.source_path
            + "\n- Destination = "
            + self.destination_path
        )

    def start(self):
        """It syncs the the destination folder to contains the songs and playlists according to the source music library."""
        print("Syncing")
        progress_weight = 0.8
        self.errors = []
        self.set_progress(0)
        self.sync_songs(progress_weight)
        self.set_progress(100 * progress_weight)
        self.sync_playlists(1 - progress_weight)
        self.set_progress(100)
        print("Sync process completed")

    def sync_songs(self, progress_weight: float = 1) -> None:
        """It syncs the destination folder to contains the songs files according to the source music library.

        Args:
            progress_weight (float, optional): Part of total that represents this sync process in the progress bar from the graphical user interface (1 means the whole progress bar and 0.5 means half of it).
        """
        print("Syncing songs")
        increment_song = 50 * progress_weight / len(self.library.songs)
        increment_artist = 50 * progress_weight / self.library.get_artists_number()
        artists = set()  # List of folder paths to library artists
        albums = {}  # List of folder paths to library albums
        songs = {}  # List of file paths to library songs
        for song in self.library.songs:
            # Folder relative path to artist
            artist = replace_special_characters(song.artist)
            # Folder relative path to album
            album = get_folder_path(song)
            # File relative path
            file = get_file_path(song)
            # Library folders
            if not artist in albums:
                albums[artist] = set()
                songs[artist] = {}
            if not album in songs[artist]:
                songs[artist][album] = set()
            artists.add(artist)
            albums[artist].add(album)
            songs[artist][album].add(file)
            # Check if the song file exists in the source folder. If not, add the song to the errors list.
            if not exists(self.source_path + SEPARATOR + file):
                self.errors.append(song)
                print(
                    "Song not found in the source folder ("
                    + self.source_path
                    + SEPARATOR
                    + file
                    + ")"
                )
            else:
                # Check if the song file exists in the destination folder. If not, copy the song file.
                if not exists(self.destination_path + SEPARATOR + file):
                    if not exists(self.destination_path + SEPARATOR + album):
                        create_dir(self.destination_path + SEPARATOR + album)
                        copy(
                            self.source_path + SEPARATOR + file,
                            self.destination_path + SEPARATOR + file,
                        )
                    else:
                        try:
                            copy(
                                self.source_path + SEPARATOR + file,
                                self.destination_path + SEPARATOR + file,
                            )
                        except:
                            self.errors.append(song)
                            print(
                                "Song could not be copied (from "
                                + self.source_path
                                + SEPARATOR
                                + file
                                + "to "
                                + self.destination_path
                                + SEPARATOR
                                + file
                                + ")"
                            )
            # Update progress bar
            self.increment_progress(increment_song)
        # Destination clean
        for artist in dir(self.destination_path):
            if not artist in artists:
                remove_tree(
                    self.destination_path + SEPARATOR + artist, ignore_errors=True
                )
            else:
                for album in dir(self.destination_path + SEPARATOR + artist):
                    album_path = artist + SEPARATOR + album
                    if not album_path in albums[artist]:
                        remove_tree(
                            self.destination_path + SEPARATOR + album_path,
                            ignore_errors=True,
                        )
                    else:
                        for song in dir(self.destination_path + SEPARATOR + album_path):
                            song_path = album_path + SEPARATOR + song
                            if not song_path in songs[artist][album_path]:
                                remove(self.destination_path + SEPARATOR + song_path)
            # Update progress bar
            self.increment_progress(increment_artist)
        print("Songs synced")

    def sync_playlists(self, progress_weight: float = 1) -> None:
        """It updates the playlists in the destination folder according to the source music library.

        Args:
            progress_weight (float, optional): Part of total that represents this sync process in the progress bar from the graphical user interface (1 means the whole progress bar and 0.5 means half of it).
        """
        print("Syncing playlists")
        increment_playlist = int(progress_weight / len(self.library.playlists))
        # Remove all prexisting playlists files from the destination folder
        if exists(self.destination_path):
            for playlist in dir(self.destination_path):
                if playlist.endswith(EXTENSION):
                    remove(join(self.destination_path, playlist))
        else:
            create_dir(self.destination_path)
        # Create playlists files
        for playlist in self.library.playlists:
            try:
                for song in playlist.get_songs():
                    # Artist without special characters
                    song_file = get_file_path(song)
                    # Create a playlist file only if it doesn't exist and add the song path to this file
                    if exists(
                        self.destination_path + SEPARATOR + playlist.name + EXTENSION
                    ):
                        mode = "a"  # Editing mode
                    else:
                        mode = "w"  # Creation mode
                    playlist_file = open(
                        self.destination_path + SEPARATOR + playlist.name + EXTENSION,
                        mode,
                    )
                    playlist_file.write(song_file + "\n")
                    playlist_file.close()
            except:
                self.errors.append(playlist)
                print(
                    "Playlist could not be created ("
                    + self.destination_path
                    + SEPARATOR
                    + playlist.name
                    + EXTENSION
                    + ")"
                )
            # Update progress bar
            self.increment_progress(increment_playlist)
        print("Playlist synced")

    def set_progress(self, progress: int) -> None:
        """It sets the progress bar to an specific percent number.

        Args:
            progress (int): Progress percent number (from 0 to 100).
        """
        if self.window:
            self.window["progress"]["value"] = progress
            self.window["root"].update()

    def increment_progress(self, progress: int) -> None:
        """It increments the progress bar a percent number.

        Args:
            progress (int): Progress percent number (from 0 to 100) to increment to the current progress.
        """
        if self.window:
            self.window["progress"]["value"] += progress
            self.window["root"].update()


def replace_special_characters(path: str) -> str:
    """It replace special characters with character _ for using in file path strings.

    Args:
        path (str): String to be replaced.

    Returns:
        str: replaced string.
    """
    return sub(SPECIAL_CHARACTERS, "_", sub(r"\/\.", "\_", path))


def get_folder_path(song: Song) -> str:
    """It gets the relative path of the song folder according to its metadata.

    Args:
        song (Song): Object of Song class containing all metadata.

    Returns:
        str: Path name to the song folder, relative to the music folder.
    """
    # Artist without special characters
    artist = sub(r"^\.|\.$", "_", replace_special_characters(song.artist))
    # Album without special characters
    album = sub(r"^\.|\.$", "_", replace_special_characters(song.album))
    # Full folder path
    return artist + SEPARATOR + album


def get_file_path(song: Song) -> str:
    """It gets the relative path of the song file according to its metadata.

    Args:
        song (Song): Object of Song class containing all metadata.

    Returns:
        str: Path name to the song file, relative to the music folder.
    """
    # Disc number
    disc_number = ""
    if song.disc_number is not None:
        disc_number = str(song.disc_number) + "-"
    # Track number with two digits
    track_number = ""
    if song.track_number:
        if song.track_number < 10:
            track_number += "0"
        track_number += str(song.track_number) + " "
    # Title without special characters
    title = replace_special_characters(song.title)
    # Full file path
    return (
        get_folder_path(song)
        + SEPARATOR
        + sub(r"^\.", "_", disc_number + track_number + title + "." + song.format)
    )
