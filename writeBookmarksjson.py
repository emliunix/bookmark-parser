# -*- coding: utf-8 -*-

from __future__ import print_function

from bmparser import *
from extractor import *
from util import *
import json

writefile("bookmarks.json", json.dumps(extract(tokenize(readfile("bookmarks.html")))))