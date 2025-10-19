#! /usr/bin/env python -B
# vi: set syntax=python ts=4 sw=4 sts=4 et ff=unix ai si :

# Simple test script that print all items from ~/Music/iTunes/iTunes Music Library.xml

import os
import sys

from itunesLibrary import library

path = os.path.join(os.getenv("HOME"), "Music/iTunes/iTunes Music Library.xml")
lib = library.parse(path, True)
musicItems = set(lib.getPlaylist("Music").items)
musicItems = sorted(
    list(musicItems),
    key=lambda k: (k.artist if k.artist else "", k.title if k.title else "", k.album if k.album else ""),
)

for item in musicItems:
    print(item)

sys.exit(0)
