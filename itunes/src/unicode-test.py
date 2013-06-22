#!/usr/bin/python
# -*- coding: utf-8 -*- 


import os,sys
from itunesLibrary import library

path = os.path.join("../../sample-data/","unicode.xml")
lib = library.parse(path)
item = lib.getItemsById("164")

print(item)

sys.exit(0)
