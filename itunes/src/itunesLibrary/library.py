"""
"""

import logging, os
from abc import ABCMeta

LOGGING_FILE = '/tmp/itunes-library.log'

def parse(pathToXMLFile):
    if os.path.exists(LOGGING_FILE):
        os.remove(LOGGING_FILE)
    logging.basicConfig(filename=LOGGING_FILE, level=logging.INFO)

    from itunesLibrary import parser
    return parser.Parser().parse(pathToXMLFile)
    
class Library(object):
    def __init__(self):
        super(Library, self).__init__()
        self.playlists = []
        self.items     = []
        
    def addPlaylist(self,playlist):
        self.playlists.append(playlist)
        
    def addItem(self,item):
        self.items.append(item)
        
    def getItemsById(self,trackId):
        for item in self.items:
            if item.getItunesAttribute('Track ID') == trackId:
                return item
        return None
        
    def getPlaylist(self,name):
        return [p for p in self.playlists if p.title == name]

    def getItemsForArtist(self,name):
        return [i for i in self.items if i.artist == name]
    
    def __iter__(self):
        return (i for i in self.items)
    
    def __len__(self):
        return len(self.items)
        
class ItunesItem(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.itunesAttibutes = dict()
        
    def setItunesAttribute(self,key,value):
        key = latin1_to_ascii(key)
        try:
            self.itunesAttibutes[key] = latin1_to_ascii(value)
        except:
            self.itunesAttibutes[key] = value
            
    def getItunesAttribute(self,key):
        key = latin1_to_ascii(key)
        return self.itunesAttibutes.get(key,None)

    def keys(self):
        return self.itunesAttibutes.keys()

    @property
    def title(self):
        return self.itunesAttibutes.get('Name',None)


class PlayList(ItunesItem):
    def __init__(self):
        super(PlayList, self).__init__()
        self.items = []

    def addItem(self,item):
        self.items.append(item)

    def __str__(self):
        return "{0} : {1}".format(self.title, len(self.items))          

    def __iter__(self):
        return (i for i in self.items)

    def __len__(self):
        return len(self.items)
    
class Item(ItunesItem):
    def __init__(self):
        super(Item, self).__init__()
    
    @property
    def artist(self):
        return self.getItunesAttribute('Artist')

    @property
    def album(self):
        return self.getItunesAttribute('Album')

    def __str__(self):
        return "{0} {1} {2}".format(self.artist, self.album, self.title)  
        
# Helper Methods
        
def latin1_to_ascii(unicode_input):
    """This takes a UNICODE string and replaces Latin-1 characters with
        something equivalent in 7-bit ASCII. It returns a plain ASCII string. 
        This function makes a best effort to convert Latin-1 characters into 
        ASCII equivalents. It does not just strip out the Latin-1 characters.
        All characters in the standard 7-bit ASCII range are preserved. 
        In the 8th bit range all the Latin-1 accented letters are converted 
        to unaccented equivalents. Most symbol characters are converted to 
        something meaningful. Anything not converted is deleted.
        http://code.activestate.com/recipes/251871/
    """
    xlate={0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y',
        0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
        0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
        0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
        0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
        0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
        0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
        0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>', 
        0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
        0xd7:'*', 0xf7:'/',
        0x2022: '*',
        0x2013: '-',
        0x2019: "'"
        }

    r = ''
    for i in unicode_input:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += str(i)
    return r

