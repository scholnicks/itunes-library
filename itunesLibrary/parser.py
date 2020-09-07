"""
Parser - Parses the iTunes XML file

(c) Steve Scholnick <scholnicks@gmail.com>
MIT License

See http://search.cpan.org/~dinomite/Mac-iTunes-Library-1.0/lib/Mac/iTunes/Library/XML.pm for Notes on the ridiculous format for the
iTunes Library XML file

Thanks to https://github.com/dinomite for deciphering the iTunes Library XML format

    https://github.com/scholnicks/itunes-library
"""

import xml.sax
from . import library

DICT_TYPE       = 'dict'
ARRAY_TYPE      = 'array'
STRING_TYPE     = 'string'
INTEGER_TYPE    = 'integer'
ITEM_ATTRIBUTES = (INTEGER_TYPE,STRING_TYPE,'date','data')

class Parser(xml.sax.ContentHandler):
    """Parses the iTunes XML file"""

    def __init__(self):
        """Constructor"""
        xml.sax.ContentHandler.__init__(self)
        self.stack                = []
        self.inPlayLists          = False
        self.inTracks             = False
        self.inMusicFolder        = False
        self.inMajorVersion       = False
        self.inMinorVersion       = False
        self.inApplicationVersion = False
        self.curKey               = ''
        self.bufferString         = ''
        self.item                 = None
        self.lib                  = None

    def parse(self,pathToXMLFile,ignoreRemoteSongs):
        """parses the XML file passed in"""
        self.lib = library.Library(ignoreRemoteSongs)
        xml.sax.parse(open(pathToXMLFile,'r', encoding="utf8"), self)
        return self.lib

    def startElement(self, name, attrs):
        """callback method for SAX parsing"""
        self.stack.append(name)

        if len(self.stack) == 1:
            self.lib.version = attrs.getValue('version')
        elif len(self.stack) == 4:
            if name == DICT_TYPE:
                if self.inPlayLists:
                    self.item = library.PlayList()
                else:
                    self.item = library.Item()

    def endElement(self, name):
        """callback method for SAX parsing"""
        depth = len(self.stack)
        self.stack.pop()

        if depth == 3:
            if name == DICT_TYPE:
                self.inTracks = False
            elif name == ARRAY_TYPE:
                self.inPlayLists = False

            if self.inMusicFolder and name == STRING_TYPE:
                self.lib.musicFolder = self.bufferString
                self.inMusicFolder = False
                self.curKey        = ''
                self.bufferString    = ''
        elif depth == 4:
            if self.item:
                if self.inPlayLists:
                    self.lib.addPlaylist(self.item)
                else:
                    self.lib.addItem(self.item)

            if name == DICT_TYPE:
                self.item = None
        elif depth == 5:
            if name in ITEM_ATTRIBUTES:
                self.item.setItunesAttribute(self.curKey,self.bufferString)
                self.curKey       = ''
                self.bufferString = ''
            elif name == 'true':
                self.item.setItunesAttribute(self.curKey,True)
                self.curKey = ''
            elif name == 'false':
                self.item.setItunesAttribute(self.curKey,False)
                self.curKey = ''
        elif depth == 7:
            if name == INTEGER_TYPE:
                track = self.lib.getItemsById(self.bufferString)
                if track:
                    self.item.addItem(track)

                self.curKey       = ''
                self.bufferString = ''

    def characters(self, content):
        """callback method for SAX parsing"""
        if len(self.stack) == 3:
            if self.stack[-1] == 'key':
                if content == 'Application Version':
                    self.inApplicationVersion = True
                elif content == 'Major Version':
                    self.inMajorVersion = True
                elif content == 'Minor Version':
                    self.inMinorVersion = True
                elif content == 'Tracks':
                    self.inTracks = True
                elif content == 'Playlists':
                    self.inPlayLists = True
            elif self.stack[-1] in ('integer','string','true','false'):
                if self.inApplicationVersion:
                    self.lib.applicationVersion = content
                    self.inApplicationVersion = False
                elif self.inMajorVersion:
                    self.lib.majorVersion = content
                    self.inMajorVersion = False
                elif self.inMinorVersion:
                    self.lib.minorVersion = content
                    self.inMinorVersion = False
                elif self.inMusicFolder:
                    self.bufferString += content if content else ''
        elif len(self.stack) == 5:
            if self.stack[-1] == 'key':
                self.curKey += content if content else ''
            elif self.stack[-1] in ITEM_ATTRIBUTES:
                self.bufferString += content if content else ''
        elif len(self.stack) == 7:
            if self.stack[-1] == 'key':
                self.curKey += content
            elif self.stack[-1] in ('integer','string','date'):
                self.bufferString += content if content else ''


