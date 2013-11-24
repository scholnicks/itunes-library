#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os,sys
from itunesLibrary import library

path = os.path.join(os.getenv("HOME"),"Music/iTunes/iTunes Music Library.xml")
lib = library.parse(path)

musicItems = set(lib.getPlaylist("Music").items)

for name in ("Steve","Laurel","Christmas"):
    musicItems -= set(lib.getPlaylist(name))

musicItems = sorted(list(musicItems),key=lambda k: (k.artist,k.title,k.album))

for item in musicItems:
    print("{0:35s} {1:40s} {2}".format(item.artist,item.title,item.album))

sys.exit(0)