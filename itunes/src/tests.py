
import os
from itunesLibrary import library

SAMPLE_DATA_DIRECTORY = "../../sample-data/"

def test_empty():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"empty.xml"))
    assert 0 == len(lib)
    
def test_artist():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    assert 10 == len(lib)
    assert "David Bowie" == lib.items[0].artist
    
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
    assert item
    assert item.album == 'The Next Day (Deluxe Version)'
    assert item.getItunesAttribute('Total Time') == '178474'
    
def test_getItemsById_Failure():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    item = lib.getItemsById("-1")
    assert not item
    
def test_getItemsById_Interger():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"10.xml"))
    item = lib.getItemsById(16116)
    assert item
    
def test_playlist():
    lib = library.parse(os.path.join(SAMPLE_DATA_DIRECTORY,"111.xml"))
    assert lib.getPlaylist("Gray")
