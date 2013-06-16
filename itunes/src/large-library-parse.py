#!/usr/bin/python
"""
My File
  Size: 4.4mb
  Lines of XML: 104,993
  No of Items: 2,413

% time python large-library-parse.py
2413

real	3m12.529s
user	3m9.469s
sys	    0m0.864s
 
Machine: Old Macbook (late 2008, 2.4 GHz Duo, 4 GB RAM)
"""

import os,sys
from itunesLibrary import library

path = os.path.join(os.getenv("HOME"),"Music/iTunes/iTunes Music Library.xml")
lib = library.parse(path)
print len(lib)
sys.exit(0)
