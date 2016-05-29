# -*- coding: utf-8 -*-

from __future__ import print_function

def readfile(fname):
    with open(fname, "r") as f:
        return f.read()
        
def writefile(fname, data):
    with open(fname, "w") as f:
        f.write(data)