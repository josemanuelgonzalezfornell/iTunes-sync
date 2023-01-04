import xml.etree.ElementTree as ElementTree


class Song:
    """Class for songs.
    """

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
        """
        assert type(
            id) is int and id >= 0, 'Song ID must be a positive integer number.'
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
        for key in metadata:
            if metadata[key] is not None:
                if key == 'rating':
                    assert metadata[key] == 0 or metadata[key] == 20 or metadata[key] == 40 or metadata[
                        key] == 60 or metadata[key] == 80 or metadata[key] == 100, 'Argument ' + key + ' is not a valid value.'
                elif key in ['track_number', 'disc_number', 'year', 'play_count']:
                    assert type(metadata[key]) is int and metadata[key] >= 0, 'Argument ' + \
                        key + ' must be a positive integer number.'
                else:
                    assert type(metadata[key]) is str, 'Argument ' + \
                        key + ' must be a string.'
                setattr(self, key, metadata[key])


class Playlist:
    """Class for playlists.
    """

    def __init__(self, id: int, name: str, songs: list = []) -> None:
        """Constructor for Playlist class.

        Args:
                id (int): ID unique number in the music library.
                name (str): Playlist name.
                songs (Song, optional): List of songs. Defaults to [].
        """
        self.id = id
        self.name = name
        self.__songs = songs
        if songs is not None:
            assert type(
                songs) is list, 'Argument songs must be a list that contains only Song objects.'
            for song in songs:
                assert song.__class__.__name__ == 'Song', 'Argument songs must be a list that contains only Song objects.'
            self._Playlist__songs = songs

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
                self._Playlist__songs), 'Index must be bewteen 0 and playlist length'
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
        return len(self._Playlist__songs)


class Library:
    """Class for music library.
    """

    def __init__(self, file_name: str = None, source: str = 'iTunes') -> None:
        """Constructor for Library class.

        Args:
                filename (str, optional): File name of the music library XML file. Defaults to None, so an empty library is created.
                source (str, optional): Application name that manages the music library XML file. Defaults to 'iTunes'.
        """
        def get_section(xml: ElementTree, key: str) -> ElementTree:
            """It returns the XML tag just after a key tag which includes a key value inside.

            Args:
                xml (ElementTree): XML content.
                key (str): Key tag name that refers the XML section to be returned.

            Returns:
                ElementTree: XML section inside the XML content to be returned.
            """
            for index, value in enumerate(xml.findall('key')):
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
        self.file_name = file_name
        if self.file_name is not None:
            library = read_XML(self.file_name)
            if source == 'iTunes':
                # Songs
                songs = get_section(library.getroot().find('dict'), 'Tracks')
                ids = songs.findall('key')
                metadata = songs.findall('dict')
                for index, song_id in enumerate(ids):
                    title = get_metadata(metadata[index], 'Name')
                    artist = get_metadata(metadata[index], 'Artist')
                    album = get_metadata(metadata[index], 'Album')
                    album_artist = get_metadata(
                        metadata[index], 'Album Artist')
                    track_number = get_metadata(
                        metadata[index], 'Track Number')
                    if track_number is not None:
                        track_number = int(track_number)
                    disc_number = get_metadata(
                        metadata[index], 'Disc Number')
                    if disc_number is not None:
                        disc_number = int(disc_number)
                    year = get_metadata(metadata[index], 'Year')
                    if year is not None:
                        year = int(year)
                    genre = get_metadata(metadata[index], 'Genre')
                    rating = get_metadata(metadata[index], 'Rating')
                    if rating is not None:
                        rating = int(rating)
                    play_count = get_metadata(metadata[index], 'Play Count')
                    if play_count is not None:
                        play_count = int(play_count)
                    self.songs.append(Song(id=int(song_id.text), title=title, artist=artist, album=album, album_artist=album_artist,
                                           track_number=track_number, disc_number=disc_number, year=year, genre=genre, rating=rating, play_count=play_count))
                # Playlists
                playlists = get_section(
                    library.getroot().find('dict'), 'Playlists').findall('dict')
                for index, playlist in enumerate(playlists):
                    items = get_section(playlist, 'Playlist Items')
                    if items:
                        playlist_name = get_metadata(playlist, 'Name')
                        if not playlist_name in ['Library', 'Downloaded', 'Music', 'Playlists', 'Rating']:
                            playlist_id = int(get_metadata(
                                playlist, 'Playlist ID'))
                            playlist_songs = []  # Playlist songs
                            songs = items.findall('dict')
                            for song in songs:
                                song_id = int(get_metadata(
                                    song, 'Track ID'))  # Song ID
                                playlist_songs.append(self.get_song(song_id))
                            self.playlists.append(
                                Playlist(playlist_id, playlist_name, playlist_songs))

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


def read_XML(file_name: str) -> ElementTree:
    """It reads a XML file and returns a xml.etree.ElementTree.ElementTree object with the XML content.

    Args:
        filename (str): Path to the XML file.

    Returns:
        ElementTree: xml.etree.ElementTree.ElementTree object with the XML content.
    """
    file = open(file_name, 'r')
    return ElementTree.parse(file_name)
    file.close()
