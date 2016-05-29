# -*- coding: utf-8 -*-

from __future__ import print_function

from bmparser import *
from extractor import *
import util

print(extract(tokenize(util.readfile("bookmarks.html"))))