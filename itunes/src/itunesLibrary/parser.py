"""Library - Represents a complete iTunes Library

(c) Steve Scholnick <steve@scholnick.net>
MIT License

See http://search.cpan.org/~dinomite/Mac-iTunes-Library-1.0/lib/Mac/iTunes/Library/XML.pm for Notes on the ridiculous format for the 
iTunes Library XML file

Thanks to https://github.com/dinomite for deciphering the iTunes Library XML format

    https://github.com/scholnicks/itunes-library
"""
import logging
import xml.sax
from itunesLibrary import library

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
        self.stack         = []
        self.inPlayLists   = False
        self.inTracks      = False
        self.inMusicFolder = False
        self.curKey        = ''
        self.bufferString  = ''
        self.item          = None

    def parse(self,pathToXMLFile):
        """parses the XML file passeed in"""
        self.filePath = pathToXMLFile
        self.lib = library.Library()
        xml.sax.parse(open(self.filePath,'r'), self)
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
                #logging.debug("Setting {0} to {1}".format(self.curKey,self.bufferString))
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
                    logging.debug("adding track " + str(track))
                    self.item.addItem(track)
                    
                self.curKey       = ''
                self.bufferString = ''
                
    def characters(self, content):
        """callback method for SAX parsing"""
        if len(self.stack) == 3:
            if self.stack[-1] == 'key':
                if content == 'Tracks':
                    self.inTracks = True
                elif content == 'Playlists':
                    self.inPlayLists = True
            elif self.stack[-1] in ('integer','string','true','false'):
                if self.inMusicFolder:
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
            

