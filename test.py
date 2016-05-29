# -*- coding: utf-8 -*-

from __future__ import print_function
from bmparser import *

testdata = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
     <DT><H3 FOLDED ADD_DATE="1464081989" LAST_MODIFIED="1464451484" PERSONAL_TOOLBAR_FOLDER="true">书签栏</H3>"""
     
def test():
    
    print("---data---\n%s\n----------" % (testdata, ))
    
    pos = 0
    length = len(testdata)
    while pos < length:
        (nextPos, result) = readUnit(testdata, pos)
        print("parsed %d:%d =>" % (pos, nextPos))
        print(result)
        pos = nextPos

test()

print("----------")

print(tokenize(testdata))