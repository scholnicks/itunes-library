#! /usr/bin/env python -B
# -*- coding: utf-8 -*-

from __future__ import print_function
import os,sys
from itunesLibrary import library

path = os.path.join(os.getenv("HOME"),"Music/iTunes/iTunes Music Library.xml")
lib = library.parse(path,True)
musicItems = set(lib.getPlaylist("Music").items)
musicItems = sorted(list(musicItems),key=lambda k: (k.artist,k.title,k.album))

for item in musicItems:
    print(item)

sys.exit(0)
