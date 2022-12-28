from musiclibrary import *
import unittest


def test_Song():
    song = Song(id=0, title='Title', artist='Artist', album='Album',
                tracknumber=1, discnumber=2, genre='Genre', rating=40)


def test_Playlist():
    playlist = Playlist(0, 'Playlist')
    song_0 = Song(id=0, title='Song 0', artist='Artist', album='Album',
                  tracknumber=1, genre='Genre', rating=40)
    song_1 = Song(id=1, title='Song 1', artist='Artist', album='Album',
                  tracknumber=1, genre='Genre', rating=40)
    song_2 = Song(id=2, title='Song 2', artist='Artist', album='Album',
                  tracknumber=1, genre='Genre', rating=40)
    playlist.addSong(song_1)
    assert playlist.getSong(0) == song_1 and playlist.getLength() == 1
    playlist.addSong(song_0, 0)
    assert playlist.getSong(0) == song_0 and playlist.getLength() == 2
    playlist.addSong(song_2)
    assert playlist.getSong(2) == song_2 and playlist.getLength() == 3
    playlist.removeSong(song_1)
    assert playlist.getSong(1) == song_2 and playlist.getLength() == 2
    playlist.removeIndex(0)
    assert playlist.getSong(0) == song_2 and playlist.getLength() == 1


def test_Library():
    print('iTunes Music library reader test')
    library = Library('iTunes Music Library.xml')
    # Songs
    song = library.songs[3]
    assert song.id == 2187
    assert song.title == 'Scumbag'
    assert song.artist == 'Green Day'
    assert song.album == 'Shenanigans'
    assert song.albumartist == 'Green Day'
    assert song.tracknumber == 8
    assert song.year == 2002
    assert song.genre == 'Garage rock'
    assert song.rating == 60
    for song in library.songs:
        if song.id == 4801:
            assert song.discnumber == 1
    # Playlists
    print('List of found playlists:')
    for index, playlist in enumerate(library.playlists):
        print(str(index) + ': ' + playlist.name)
    playlist = library.playlists[6]
    assert playlist.id == 12991
    assert playlist.name == 'Christmas'
    assert playlist.getLength() == 9
    assert playlist.getSongs()[1].id == 4613
    assert playlist.getSongs()[1].title == 'Can\'t take my eyes off you'
