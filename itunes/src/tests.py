import os
from itunesLibrary import library

SAMPLE_DATA_DIRECTORY = "../../sample-data/"

def test_empty():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"empty.xml"))
    assert 0 == len(lib)

def test_applicationVersion():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"empty.xml"))
    assert "11.0.2" == lib.applicationVersion

def test_minorVersion():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"empty.xml"))
    assert "1" == lib.minorVersion

def test_majorVersion():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"empty.xml"))
    assert "2" == lib.majorVersion

def test_playlists():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert lib.playlists

def test_library_items():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert lib.items

def test_playlist_items():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert lib.playlists[0].items

def test_iter():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert lib.__iter__()

def test_playlist_iter():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert lib.__iter__().__iter__()

def test_length():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert 10 == len(lib)

def test_artist():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert "David Bowie" == lib.items[0].artist

def test_album():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert "The Next Day (Deluxe Version)" == lib.items[0].album

def test_title():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert "The Next Day" == lib.items[0].title

def test_getItemsForArtist():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert lib.getItemsForArtist("David Bowie")

def test_getItemsForArtist_Failure():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    items = lib.getItemsForArtist("Not There")
    assert items == []

def test_getItemsById():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    item = lib.getItemsById("16116")
    assert item.album == 'The Next Day (Deluxe Version)' and item.getItunesAttribute('Total Time') == '178474'

def test_totalTime():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    item = lib.getItemsById("16116")
    assert item.getItunesAttribute('Total Time') == '178474'

def test_getItemsById_Failure():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    item = lib.getItemsById("-1")
    assert not item

def test_getItemsById_Integer():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    item = lib.getItemsById(16116)
    assert item

def test_playlist():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"111.xml"))
    playlist = lib.getPlaylist("Gray")
    assert len(playlist)  # it has items

def test_unicode_title():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"unicode.xml"))
    item = lib.getItemsById("164")
    assert item.title
    assert item.artist == 'Blackfield'
