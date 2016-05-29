# -*- coding: utf-8 -*-

from __future__ import print_function

from bmparser import *
from extractor import *

testdata = "<TITLE>Bookmarks</TITLE>"

print(extractTitle(TokenIter(tokenize(testdata))))