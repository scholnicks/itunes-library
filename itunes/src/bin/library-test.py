#!/usr/bin/python -BO

import sys
#sys.path.append('/Users/steve/development/iTunesLibrary')

from itunesLibrary import library

def main(path):
    lib = library.Library.parse(path)
    for p in lib.playlists:
        print(p.title)
        
    print lib.getPlaylist('Library')
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1])
