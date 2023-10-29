from platform import platform as get_os
from src.music_library import *
from io import open
from os.path import exists, join
from os import makedirs as create_dir
from os import remove
from os import listdir as dir
from shutil import copy2 as copy
from shutil import rmtree as remove_tree


class Sync:
    """Class to sync the library."""

    library: Library = None  # Source music library XML file.
    source_folder: str = None  # Absolute folder path to the source music folder.
    destination_folder: str = (
        None  # Absolute folder path to the destination music folder.
    )
    destination_playlists: str = None  # Absolute file path to the destination playlists XML file (only if destination language is Rhythmbox).
    window: set = None  # Graphical user interface object.
    errors: set = []  # Songs and playlists that could not be synced.

    def __init__(
        self,
        source_language: str,
        source_files: list,
        source_folder: str,
        destination_folder: str,
        destination_playlists: str = None,
        window: set = None,
    ) -> None:
        """It creates a sync process.

        Args:
            source_language (str): Library language for the source XML files.
            source_files (list): Absolute file path to the source music library XML files.
            source_folder (str): Absolute folder path to the source music folder.
            destination_folder (str): Absolute folder path to the destination music folder.
            destination_playlists (str): Absolute file path to the destination playlists XML file (only if destination language is Rhythmbox). Defaults to None.
            window (set, optional): Graphical user interface object.
        """
        self.library = Library(source_files, language=source_language)
        self.source_language = source_language
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.destination_playlists = destination_playlists
        self.window = window
        message = "Sync process created:"
        message += "\n- Source language = " + source_language
        message += "\n- Source library = " + self.library.files[0]
        if source_language == "Rhythmbox":
            message += "\n- Source playlists = " + self.library.files[1]
        message += "\n- Source folder = " + self.source_folder
        message += "\n- Destination folder = " + self.destination_folder
        if self.destination_playlists:
            message += "\n- Destination playlists = " + self.destination_playlists
        print(message)

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
        is_windows = get_os()[:7] == "Windows"
        for song in self.library.songs:
            # Folder relative path to artist
            artist = sub(r"^\.|\.$", "_", replace_special_characters(song.artist))
            # Folder relative path to album
            album = get_folder_path(song)
            # File relative path
            source_file = get_file_path(
                song, self.source_language == "iTunes" and is_windows
            )
            destination_file = get_file_path(song)
            # Library folders
            if not artist in albums:
                albums[artist] = set()
                songs[artist] = {}
            if not album in songs[artist]:
                songs[artist][album] = set()
            artists.add(artist)
            albums[artist].add(album)
            songs[artist][album].add(destination_file)
            # Check if the song file exists in the source folder. If not, add the song to the errors list.
            if not exists(self.source_folder + SEPARATOR + source_file):
                self.errors.append(song)
                print(
                    "Song not found in the source folder ("
                    + self.source_folder
                    + SEPARATOR
                    + source_file
                    + ")"
                )
            else:
                # Check if the song file exists in the destination folder. If not, copy the song file.
                if not exists(self.destination_folder + SEPARATOR + destination_file):
                    if not exists(self.destination_folder + SEPARATOR + album):
                        create_dir(self.destination_folder + SEPARATOR + album)
                        copy(
                            self.source_folder + SEPARATOR + source_file,
                            self.destination_folder + SEPARATOR + destination_file,
                        )
                    else:
                        try:
                            copy(
                                self.source_folder + SEPARATOR + source_file,
                                self.destination_folder + SEPARATOR + destination_file,
                            )
                        except:
                            self.errors.append(song)
                            print(
                                "Song could not be copied (from "
                                + self.source_folder
                                + SEPARATOR
                                + source_file
                                + "to "
                                + self.destination_folder
                                + SEPARATOR
                                + destination_file
                                + ")"
                            )
            # Update progress bar
            self.increment_progress(increment_song)
        # Destination clean
        for artist in dir(self.destination_folder):
            if not artist in artists:
                remove_tree(
                    self.destination_folder + SEPARATOR + artist, ignore_errors=True
                )
            else:
                for album in dir(self.destination_folder + SEPARATOR + artist):
                    album_path = artist + SEPARATOR + album
                    if not album_path in albums[artist]:
                        remove_tree(
                            self.destination_folder + SEPARATOR + album_path,
                            ignore_errors=True,
                        )
                    else:
                        for song in dir(
                            self.destination_folder + SEPARATOR + album_path
                        ):
                            song_path = album_path + SEPARATOR + song
                            if not song_path in songs[artist][album_path]:
                                remove(self.destination_folder + SEPARATOR + song_path)
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
        ENCODING = "utf-8"  # File encoding
        EXTENSION = ".m3u"  # Generic playlist file extension
        # Remove all prexisting playlists files from the destination folder
        if exists(self.destination_folder):
            for playlist in dir(self.destination_folder):
                if playlist.endswith(EXTENSION):
                    remove(join(self.destination_folder, playlist))
        else:
            create_dir(self.destination_folder)
        if self.destination_playlists:
            if exists(self.destination_playlists):
                remove(self.destination_playlists)
        # Create playlist file
        if self.destination_playlists:
            playlist_file = open(
                self.destination_playlists, mode="w", encoding=ENCODING
            )
            playlist_file.write('<?xml version="1.0"?>\n<rhythmdb-playlists>')
        # Fill playlists files
        for playlist in self.library.playlists:
            # Language = Generic
            if self.destination_playlists is None:
                playlist_path = (
                    self.destination_folder
                    + SEPARATOR
                    + replace_special_characters(playlist.name)
                    + EXTENSION
                )
                try:
                    # Create a playlist file only if it doesn't exist and add the song path to this file
                    if exists(playlist_path):
                        mode = "a"  # Editing mode
                    else:
                        mode = "w"  # Creation mode
                    playlist_file = open(
                        playlist_path,
                        mode=mode,
                        encoding=ENCODING,
                    )
                    playlist_file.write("\n".join(playlist.get_files()))
                    playlist_file.close()
                except:
                    self.errors.append(playlist)
                    print("Playlist could not be created (" + playlist_path + ")")
            # Language = Rhythmbox
            else:
                playlist_file.write(
                    '\n  <playlist name="'
                    + str2html(playlist.name)
                    + '" show-browser="true" browser-position="'
                    + str(playlist.id)
                    + '" search-type="search-match" type="static">'
                    + "\n    <location>"
                    + "</location>\n    <location>".join(
                        playlist.get_urls(folder=self.destination_folder)
                    )
                    + "</location>"
                    + "\n  </playlist>"
                )
            # Update progress bar
            self.increment_progress(increment_playlist)
        # Close playlist file
        if self.destination_playlists:
            playlist_file.write("\n</rhythmdb-playlists>")
            playlist_file.close()
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
