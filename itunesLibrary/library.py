"""Library - Represents a complete iTunes Library

(c) Steve Scholnick <scholnicks@gmail.com>
MIT License

    https://github.com/scholnicks/itunes-library
"""

from abc import ABCMeta

def parse(pathToXMLFile, ignoreRemoteSongs=True):
    """Main method for constructor a Library object"""
    from . import parser
    return parser.Parser().parse(pathToXMLFile,ignoreRemoteSongs)


class Library(object):
    """Represents a complete iTunes Library"""

    def __init__(self,ignoreRemoteSongs):
        """Constructor"""
        super(Library, self).__init__()
        self.playlists = []
        self.items     = []
        self.ignoreRemoteSongs = ignoreRemoteSongs

    def addPlaylist(self,playlist):
        """Adds a playlist"""
        self.playlists.append(playlist)

    def addItem(self,item):
        """Adds an item"""
        if self.ignoreRemoteSongs and item.remote:
            return

        self.items.append(item)

    def getItemsById(self,trackId):
        """Returns an item based on its Track Idor None"""
        trackId = str(trackId)      # all keys are strs, allow for integers to be passed in
        return next((i for i in self.items if i.getItunesAttribute('Track ID') == trackId),None)

    def getPlaylist(self,name):
        """Returns a Playlist based on its name or None"""
        playlist = self.getAllPlaylists(name)
        return playlist[0] if playlist else None

    def getAllPlaylists(self,name):
        """Returns all playlists that match the name or an empty list"""
        return [p for p in self.playlists if p.title == name]

    def getItemsForArtist(self,name):
        """Returns all items for an artist as a List"""
        return [i for i in self.items if i.artist == name]

    def __iter__(self):
        """Allows for quick iteration through the items"""
        return iter(self.items)

    def __len__(self):
        """returns the number of items stored in the library"""
        return len(self.items)


class ItunesItem(object):
    """Abstract Base Class for iTunes items stored in the library"""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor"""
        self.itunesAttibutes = dict()

    def setItunesAttribute(self,key,value):
        """Sets an iTunes attribute"""
        self.itunesAttibutes[key] = value

    def getItunesAttribute(self,key):
        """Returns an iTunes attribute"""
        return self.itunesAttibutes.get(key,None)

    def keys(self):
        """Returns all of the possible iTunes attribute keys"""
        return self.itunesAttibutes.keys()

    @property
    def title(self):
        """Returns the title"""
        return self.getItunesAttribute('Name')

    @property
    def remote(self):
        '''returns if the song is remote'''
        return self.getItunesAttribute('Track Type') == 'Remote'


class PlayList(ItunesItem):
    """an iTunes Playlist"""

    def __init__(self):
        """Constructor"""
        super(PlayList, self).__init__()
        self.items = []

    def addItem(self,item):
        """Adds an item"""
        self.items.append(item)

    def __str__(self):
        """Returns a nice string representation"""
        return "{0}: {1}".format(self.title.encode('utf-8'), len(self.items))

    def __repr__(self):
        """Returns a possible internal representation of this object"""
        return str(self.__dict__)

    def __iter__(self):
        """Allows for quick iteration through the items"""
        return iter(self.items)

    def __len__(self):
        """returns the number of items stored in this playlist"""
        return len(self.items)


class Item(ItunesItem):
    """an item stored in the iTunes Playlist"""

    def __init__(self):
        """Constructor"""
        super(Item, self).__init__()

    @property
    def artist(self):
        """Returns the title"""
        return self.getItunesAttribute('Artist')

    @property
    def album(self):
        """Returns the album name"""
        return self.getItunesAttribute('Album')

    def __repr__(self):
        """Returns a possible internal representation of this object"""
        return str(self.__dict__)

    def __str__(self):
        """Returns a nice string representation"""
        artist = self.artist if self.artist else ''
        album  = self.album  if self.album  else ''
        title  = self.title  if self.title  else ''
        return "{0} {1} {2}".format(artist,album,title)
