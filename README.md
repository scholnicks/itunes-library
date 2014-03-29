itunes-library
==============

itunes-library represents an iTunes Library. It allows the caller to retrieve items, playlists, etc.

itunes-library is a port of Drew Stephen's excellent Perl module, http://search.cpan.org/~dinomite/Mac-iTunes-Library. The Perl 
library will be **not** re-created verbatim.

License : http://www.scholnick.net/license.txt

Installation : pip install itunesLibrary

Example Code

```python
import os
from itunesLibrary import library

path = os.path.join(os.getenv("HOME"),"Music/iTunes/iTunes Music Library.xml")

# must first parse...
lib = library.parse(path)

print len(lib)    # number of items stored

for playlist in lib.playlists:
    for item in playlist.items:
        print item          # perform function on each item in the playlist
        
# get a single playlist
playlist = lib.getPlaylist("Gray")

# get a list of all of the David Bowie songs 
bowie_items = lib.getItemsForArtist("David Bowie")

# get a single song
single_song = lib.getItemsById("16116") 

# get the iTunes application version
print lib.applicationVersion
```
