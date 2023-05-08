import xml.etree.ElementTree as ElementTree
from re import sub
from html import escape as str2html
from html import unescape as html2str
from urllib.parse import quote as str2url
from urllib.parse import unquote as url2str


SEPARATOR = "/"  # Files
SPECIAL_CHARACTERS = (
    r'\/|\\|\?|\*|@|\$|€|=|:|~|\[|\]|{|}|<|>|\^|"|´|’'  # Special characters
)
SAFE_CHARACTERS = "'" + SEPARATOR  # Characters that will not be converted to URL format
LANGUAGES = {
    "source": ["iTunes", "Rhythmbox"],
    "destination": ["Generic", "Rhythmbox"],
}  # Library languages for XML files


class Song:
    """Class for songs."""

    def __init__(self, id: int, **metadata) -> None:
        """Constructor for Song class.

        Args:
            id (int): ID unique number in the music library
            title (str): Song title
            artist (str): Artist name
            album (str): Album name
            album_artist (str): Album artist
            track_number (int): Track number in album
            disc_number (int): Disc number in album
            year (int): Year number
            genre (str): Song genre
            rating (int): Rating number (from 0 to 100). Defaults to 0.
            play_count (int): User play count. Defaults to 0.
            format (str): File format extension. Defaults to mp3.
        """
        assert type(id) is int and id >= 0, "Song ID must be a positive integer number."
        self.id = id
        self.title = None
        self.artist = None
        self.album = None
        self.album_artist = None
        self.track_number = None
        self.disc_number = None
        self.year = None
        self.genre = None
        self.rating = 0
        self.play_count = 0
        self.format = "mp3"
        for key in metadata:
            if metadata[key] is not None:
                if key == "rating":
                    assert type(metadata[key]) is int and metadata[key] in range(
                        0, 6
                    ), ("Argument " + key + " is not a valid value.")
                elif key in ["track_number", "disc_number", "year", "play_count"]:
                    assert type(metadata[key]) is int and metadata[key] >= 0, (
                        "Argument " + key + " must be a positive integer number."
                    )
                else:
                    assert type(metadata[key]) is str, (
                        "Argument " + key + " must be a string."
                    )
                setattr(self, key, metadata[key])


class Playlist:
    """Class for playlists."""

    def __init__(
        self, id: int, name: str, songs: list = None, files: list = None
    ) -> None:
        """Constructor for Playlist class.

        Args:
            id (int): ID unique number in the music library.
            name (str): Playlist name.
            songs (list, optional): List of Song objects. Defaults to None.
            files (list, optional): List of relative paths to song files. Defaults to None.
        """
        if songs is None and files is None:
            songs = []
        self.id = id
        self.name = name
        self.__songs = songs
        self.__files = files
        if songs is not None:
            assert (
                type(songs) is list
            ), "Argument songs must be a list that contains only Song objects."
            for song in songs:
                assert (
                    song.__class__.__name__ == "Song"
                ), "Argument songs must be a list that contains only Song objects."
            self._Playlist__songs = songs
        elif files is not None:
            assert (
                type(files) is list
            ), "Argument files must be a list that contains only strings."
            for file in files:
                assert (
                    type(file) is str
                ), "Argument files must be a list that contains only strings."
            self._Playlist__files = files

    def get_song(self, index: int) -> Song:
        """It gets a Song object specified by its order index in the playlist.

        Args:
            index (int): Order index in the playlist.

        Returns:
            Song: Song object.
        """
        return self.get_songs()[index]

    def get_songs(self) -> list:
        """It gets all songs in the playlist as a list object.

        Returns:
            list: List of songs in the playlist.
        """
        return self._Playlist__songs

    def add_song(self, song: Song, index: int = None) -> None:
        """It adds a Song object to the playlist in the specified order index (or at the end if no index is specified).

        Args:
            song (Song): Song object.
            index (int, optional): Order index where the song is added. Defaults adds the song at the end of the playlist.
        """
        if index is None:
            self._Playlist__songs.append(song)
        else:
            assert 0 <= index and index < len(
                self._Playlist__songs
            ), "Index must be bewteen 0 and playlist length"
            self._Playlist__songs.insert(index, song)

    def remove_song(self, song: Song) -> None:
        """It removes a song from the playlist by passing the Song object.

        Args:
            song (Song): Song object to be removed from the playlist.
        """
        self.remove_index(self.get_index(song))

    def get_index(self, song: Song) -> int:
        """It gets the order index of a Song object in the playlist.

        Args:
            song (Song): Song object

        Returns:
            int: Order index of the song in the playlist.
        """
        for index in range(0, self.get_length()):
            if self._Playlist__songs[index] == song:
                return index

    def remove_index(self, index: int) -> None:
        """It removes a song from the playlist by specifying the order index of the song in the playlist.

        Args:
            index (int): Order index of the song in the playlist.
        """
        del self._Playlist__songs[index]

    def get_length(self) -> int:
        """It returns the number of songs in the playlist.

        Returns:
            int: Number of songs in the playlist.
        """
        return len(self._Playlist__songs or self._Playlist__files)

    def get_files(self, folder: str = None) -> list:
        """It gets all file paths to songs in the playlist as a list object.

        Args:
            folder (str, optional): Music folder path. If no value is given, it returns as relative file paths. Defaults to None.

        Returns:
            list: List of file paths to songs files in the playlist.
        """
        if folder:
            if folder[-1] != SEPARATOR:
                folder += SEPARATOR
        else:
            folder = ""
        # Songs
        if not self.get_songs() is None:
            files = []
            for song in self.get_songs():
                files.append(folder + get_file_path(song))
        # Files
        elif not self.__files is None:
            files = []
            for file in self.__files:
                files.append(folder + file)
        return files

    def get_urls(self, folder: str) -> list:
        """It gets all URL paths to songs in the playlist as a list object.

        Args:
            folder (str): Music folder path.

        Returns:
            list: List of URL paths to songs files in the playlist.
        """
        PROTOCOL = "file://"
        if folder[-1] != SEPARATOR:
            folder += SEPARATOR
        # Songs
        if not self.get_songs() is None:
            urls = []
            for song in self.get_songs():
                urls.append(
                    PROTOCOL
                    + str2url(folder + get_file_path(song), safe=SAFE_CHARACTERS)
                )
        # Files
        elif not self.__files is None:
            urls = []
            for file in self.__files:
                urls.append(PROTOCOL + str2url(folder + file, safe=SAFE_CHARACTERS))
        return urls


class Library:
    """Class for music library."""

    def __init__(self, files: list = [], language: str = "iTunes") -> None:
        """Constructor for Library class.

        Args:
            files (list, optional): File name of the music library XML files. Defaults to empty list, so an empty library is created.
            language (str, optional): Library language for the XML files. Defaults to 'iTunes'.
        """

        def get_property(xml: ElementTree, key: str) -> ElementTree:
            """It returns the value of a XML tag inside of another XML tag.

            Args:
                xml (ElementTree): Parent XML tag.
                key (str): Children XML tag key.

            Returns:
                ElementTree: Value of the children XML tag.
            """
            if xml.find(key) is not None:
                return xml.find(key).text

        def get_section(xml: ElementTree, key: str) -> ElementTree:
            """It returns the XML tag just after a key tag which includes a key value inside.

            Args:
                xml (ElementTree): XML content.
                key (str): Key tag name that refers the XML section to be returned.

            Returns:
                ElementTree: XML section inside the XML content to be returned.
            """
            for index, value in enumerate(xml.findall("key")):
                if value.text == key:
                    return xml[2 * index + 1]

        def get_metadata(xml: ElementTree, key: str) -> str:
            """It returns the metadata value defined just after a key tag included in a song metadata of a iTunes XML header.

            Args:
                xml (ElementTree): XML content.
                key (str): Key tag name that refers the metadata to be returned.

            Returns:
                str: metadata value inside the XML content to be returned.
            """
            value = get_section(xml, key)
            if value is not None:
                return value.text

        self.songs = []  # List of songs (objects of Song class)
        self.playlists = []  # List of playlists (objects of Playlist class)
        self.files = files
        if self.files is not None:
            if language == "iTunes":
                library = read_XML(self.files[0])
                # Songs
                songs = get_section(library.getroot().find("dict"), "Tracks")
                ids = songs.findall("key")
                songs = songs.findall("dict")
                for song, song_id in enumerate(ids):
                    title = get_metadata(songs[song], "Name")
                    artist = get_metadata(songs[song], "Artist")
                    album = get_metadata(songs[song], "Album")
                    album_artist = get_metadata(songs[song], "Album Artist")
                    track_number = get_metadata(songs[song], "Track Number")
                    if track_number is not None:
                        track_number = int(track_number)
                    disc_number = get_metadata(songs[song], "Disc Number")
                    if disc_number is not None:
                        disc_number = int(disc_number)
                    year = get_metadata(songs[song], "Year")
                    if year is not None:
                        year = int(year)
                    genre = get_metadata(songs[song], "Genre")
                    rating = get_metadata(songs[song], "Rating")
                    if rating is not None:
                        rating = int(int(rating) / 20)
                    play_count = get_metadata(songs[song], "Play Count")
                    if play_count is not None:
                        play_count = int(play_count)
                    format = get_metadata(songs[song], "Location").split(".")[-1]
                    self.songs.append(
                        Song(
                            id=int(song_id.text),
                            title=title,
                            artist=artist,
                            album=album,
                            album_artist=album_artist,
                            track_number=track_number,
                            disc_number=disc_number,
                            year=year,
                            genre=genre,
                            rating=rating,
                            play_count=play_count,
                            format=format,
                        )
                    )
                # Playlists
                playlists = get_section(
                    library.getroot().find("dict"), "Playlists"
                ).findall("dict")
                for song, playlist in enumerate(playlists):
                    items = get_section(playlist, "Playlist Items")
                    if items:
                        playlist_name = get_metadata(playlist, "Name")
                        if not playlist_name in [
                            "Library",
                            "Downloaded",
                            "Music",
                            "Playlists",
                            "Rating",
                        ]:
                            playlist_id = int(get_metadata(playlist, "Playlist ID"))
                            playlist_songs = []  # Playlist songs
                            songs = items.findall("dict")
                            for song in songs:
                                song_id = int(get_metadata(song, "Track ID"))  # Song ID
                                playlist_songs.append(self.get_song(song_id))
                            self.playlists.append(
                                Playlist(
                                    playlist_id, playlist_name, songs=playlist_songs
                                )
                            )
            elif language == "Rhythmbox":
                # Songs
                songs = read_XML(self.files[0]).getroot().findall("entry")
                for song_id, song in enumerate(songs):
                    if song.attrib["type"] == "song":
                        title = get_property(song, "title")
                        artist = get_property(song, "artist")
                        album = get_property(song, "album")
                        track_number = get_property(song, "track-number")
                        if track_number is not None:
                            track_number = int(track_number)
                        disc_number = get_property(song, "disc-number")
                        if disc_number is not None:
                            disc_number = int(disc_number)
                        genre = get_property(song, "genre")
                        rating = get_property(song, "rating")
                        if rating is not None:
                            rating = int(rating)
                        play_count = get_property(song, "play-count")
                        if play_count is not None:
                            play_count = int(play_count)
                        format = get_property(song, "location").split(".")[-1]
                        self.songs.append(
                            Song(
                                id=int(song_id),
                                title=title,
                                artist=artist,
                                album=album,
                                track_number=track_number,
                                disc_number=disc_number,
                                genre=genre,
                                rating=rating,
                                play_count=play_count,
                                format=format,
                            )
                        )
                # Playlists
                playlists = read_XML(self.files[1]).getroot().findall("playlist")
                for playlist in playlists:
                    playlist_name = html2str(playlist.attrib["name"])
                    playlist_id = int(playlist.attrib["browser-position"])
                    playlist_songs = []
                    songs = playlist.findall("location")
                    for song in songs:
                        playlist_songs.append(
                            SEPARATOR.join(url2str(song.text).split(SEPARATOR)[-3:])
                        )
                    self.playlists.append(
                        Playlist(playlist_id, playlist_name, files=playlist_songs)
                    )

    def get_song(self, id: int) -> Song:
        """It gets a Song object specified by its ID number in the library.

        Args:
            id (int): ID number of the song in the library.

        Returns:
            Song: Song object.
        """
        for song in self.songs:
            if song.id == id:
                return song

    def get_artists_number(self) -> int:
        """It gets the number of artists in the library.

        Returns:
            int: Number of artists.
        """
        artists = set()
        for song in self.songs:
            artists.add(song.artist)
        return len(artists)

    def get_albums_number(self) -> int:
        """It gets the number of albums in the library.

        Returns:
            int: Number of albums.
        """
        albums = set()
        for song in self.songs:
            albums.add(song.album)
        return len(albums)

    def get_playlist(self, name: str) -> Playlist:
        """It gets a Playlist object specified by its name in the library.

        Args:
            name (str): Name of the playlist.

        Returns:
            Playlist: Playlist object.
        """
        for playlist in self.playlists:
            if playlist.name == name:
                return playlist


# Music file system


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


def read_XML(file_name: str) -> ElementTree:
    """It reads a XML file and returns a xml.etree.ElementTree.ElementTree object with the XML content.

    Args:
        filename (str): Path to the XML file.

    Returns:
        ElementTree: xml.etree.ElementTree.ElementTree object with the XML content.
    """
    file = open(file_name, mode="r", encoding="utf-8")
    xml = ElementTree.parse(file_name)
    file.close()
    return xml
