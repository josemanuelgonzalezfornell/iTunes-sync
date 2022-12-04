import xml.etree.ElementTree as ElementTree


class Song:
    "Class for songs."
    id: int = None  # ID number of the music library
    title: str = None  # Song title
    artist: str = None  # Artist name
    album: str = None  # Album name
    albumartist: str = None  # Album artist
    tracknumber: int = None  # Track number in album
    year: int = None  # Year number
    genre: str = None  # Song genre
    rating: int = 0  # Rating number (from 0 to 100)
    playcount: int = 0  # User play counts

    def __init__(self, id, **metadata) -> None:
        assert type(
            id) is int and id >= 0, 'Song ID must be a positive integer number.'
        self.id = id
        for key in metadata:
            if metadata[key] is not None:
                if key == 'rating':
                    assert metadata[key] == 0 or metadata[key] == 20 or metadata[key] == 40 or metadata[
                        key] == 60 or metadata[key] == 80 or metadata[key] == 100, 'Argument ' + key + ' is not a valid value.'
                elif key in ['tracknumber', 'year', 'playcount']:
                    assert type(metadata[key]) is int and metadata[key] >= 0, 'Argument ' + \
                        key + ' must be a positive integer number.'
                else:
                    assert type(metadata[key]) is str, 'Argument ' + \
                        key + ' must be a string.'
                setattr(self, key, metadata[key])


class Playlist:
    "Class for playlists."
    id: int = None
    name: str = None
    __songs = []

    def __init__(self, id: int, name: str, songs=None) -> None:
        self.id = id
        self.name = name
        if songs is not None:
            assert type(
                songs) is list, 'Argument songs must be a list that contains only Song objects.'
            for song in songs:
                assert song.__class__.__name__ == 'Song', 'Argument songs must be a list that contains only Song objects.'
            self._Playlist__songs = songs

    def getSong(self, index: int) -> Song:
        # It gets a Song object specified by its order index in the playlist.
        return self.getSongs()[index]

    def getSongs(self) -> list:
        # It gets all songs in the playlist as a list object.
        return self._Playlist__songs

    def addSong(self, song: Song, index: int = None):
        # It adds a Song object to the playlist in the specified order index (or at the end if no index is specified).
        if index is None:
            self._Playlist__songs.append(song)
        else:
            assert 0 <= index and index < len(
                self._Playlist__songs), 'Index must be bewteen 0 and playlist length'
            self._Playlist__songs.insert(index, song)

    def removeSong(self, song: Song):
        # It removes a song from the playlist by passing the Song object.
        self.removeIndex(self.getIndex(song))

    def getIndex(self, song: Song) -> int:
        # It gets the order index of a Song object in the playlist.
        for index in range(0, self.getLength()):
            if self._Playlist__songs[index] == song:
                return index

    def removeIndex(self, index: int):
        # It removes a song from the playlist by specifying the index order of the song in the playlist.
        del self._Playlist__songs[index]

    def getLength(self) -> int:
        # It returns the number of songs in the playlist.
        return len(self._Playlist__songs)


class Library:
    "Class for music library."
    filename: str = None
    songs: list = []
    playlists: list = []

    def __init__(self, filename: str, source: str = 'iTunes') -> None:
        def getSection(xml, key: str):
            # It returns the XML tag just after a key tag which includes a key value inside.
            for index, value in enumerate(xml.findall('key')):
                if value.text == key:
                    return xml[2 * index + 1]

        def getMetadata(xml, key: str) -> str:
            # It returns the metadata value defined just after a key tag included in a song metadata of a iTunes XML header.
            value = getSection(xml, key)
            if value is not None:
                return value.text

        self.filename = filename
        if self.filename is not None:
            library = readXML(self.filename)
            if source == 'iTunes':
                # Songs
                songs = getSection(library.getroot().find('dict'), 'Tracks')
                ids = songs.findall('key')
                metadata = songs.findall('dict')
                for index, song_id in enumerate(ids):
                    title = getMetadata(metadata[index], 'Name')
                    artist = getMetadata(metadata[index], 'Artist')
                    album = getMetadata(metadata[index], 'Album')
                    albumartist = getMetadata(
                        metadata[index], 'Album Artist')
                    tracknumber = getMetadata(
                        metadata[index], 'Track Number')
                    if tracknumber is not None:
                        tracknumber = int(tracknumber)
                    year = getMetadata(metadata[index], 'Year')
                    if year is not None:
                        year = int(year)
                    genre = getMetadata(metadata[index], 'Genre')
                    rating = getMetadata(metadata[index], 'Rating')
                    if rating is not None:
                        rating = int(rating)
                    playcount = getMetadata(metadata[index], 'Play Count')
                    if playcount is not None:
                        playcount = int(playcount)
                    self.songs.append(Song(id=int(song_id.text), title=title, artist=artist, album=album, albumartist=albumartist,
                                      tracknumber=tracknumber, year=year, genre=genre, rating=rating, playcount=playcount))
                # Playlists
                playlists = getSection(
                    library.getroot().find('dict'), 'Playlists').findall('dict')
                for index, playlist in enumerate(playlists):
                    items = getSection(playlist, 'Playlist Items')
                    if items:
                        playlist_name = getMetadata(playlist, 'Name')
                        if not playlist_name in ['Library', 'Downloaded', 'Music', 'Playlists', 'Rating']:
                            playlist_id = int(getMetadata(
                                playlist, 'Playlist ID'))
                            playlist_songs = []  # Playlist songs
                            songs = items.findall('dict')
                            for song in songs:
                                song_id = int(getMetadata(
                                    song, 'Track ID'))  # Song ID
                                playlist_songs.append(self.getSong(song_id))
                            self.playlists.append(
                                Playlist(playlist_id, playlist_name, playlist_songs))

    def getSong(self, id: int) -> Song:
        # It gets a Song object specified by its ID number in the library.
        for song in self.songs:
            if song.id == id:
                return song


def readXML(filename: str):
    """It reads a XML file and returns a xml.etree.ElementTree.ElementTree object with the XML content.

    Args:
            filename (str): path to the XML file.
    """
    file = open(filename, 'r')
    return ElementTree.parse(filename)
    file.close()
