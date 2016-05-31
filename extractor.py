# -*- coding: utf-8 -*-

from __future__ import print_function

from bmparser import *

ignoreTags = {"META", "HR"}

class TokenIter(object):
    '''
    Utility class to work with tokens
    '''
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.length = len(self.tokens)
        self.pos_marks = []

    def next(self):
        '''
        retrive next token
        '''
        while self.position < self.length:
            tok = self.tokens[self.position]
            self.position += 1
            if not (tok[0] == Type.TAG and tok[1] in ignoreTags):
                return tok
        return None

    def peek(self):
        return self.tokens[self.position]

    def moveBack(self):
        self.position -= 1

    def mark(self):
        self.pos_marks.append(self.position)

    def ok(self):
        self.pos_marks.pop()

    def unmark(self):
        self.position = self.pos_marks.pop()

def debugError(msg, tok):
    print("%s\n%s\n" % (msg, str(tok)))

def extract(tokens):
    tokens = TokenIter(tokens)
    
    v = executor([
        lambda: extractTitle(tokens),
        lambda: extractH1(tokens),
        lambda: extractItems(tokens)
    ])
    if v == None:
        return None
        
    (title, h1, items) = v
    return {
        "name": h1,
        "type": "folder",
        "children": items
    }
    
def executor(tasks):
    ret = []
    for t in tasks:
        v = t()
        if v == None:
            return None
        ret.append(v)
    return tuple(ret)
    
def extractTitle(toks):
    toks.mark()
    
    v = match(toks, [
        (Type.TAG, "TITLE"),
        (Type.STRING, ),
        (Type.CLOSETAG, "TITLE")
    ])
    if not v == None:
        toks.ok()
        return toStr(v[1])
    else:
        toks.unmark()
        debugError("Error parsing title ", toks.peek())
        return None
        
def extractH1(toks):
    toks.mark()
    v = match(toks, [
        (Type.TAG, "H1"),
        (Type.STRING, ),
        (Type.CLOSETAG, "H1")
    ])
    if not v == None:
        toks.ok()
        return toStr(v[1])
    else:
        toks.unmark()
        debugError("Error parsing H1 ", toks.peek())
        return None

def extractItems(toks):
    toks.mark()
    
    # test items block start mark <DL><P>
    v = match(toks, [
        (Type.TAG, "DL"),
        (Type.TAG, "P")
    ])
    if v == None:
        toks.unmark()
        debugError("Error parsing items block starting part ", toks.peek())
        return None
    
    items = []
    while True:
        # try to get an item
        v = match(toks, [
            (Type.TAG, "DT"),
            (Type.TAG, "A"),
            (Type.STRING, ),
            (Type.CLOSETAG, "A")
        ])
        # no item got, exit
        if v == None:
            debugError("Failed attempting to get an Item. Try to get a folder", toks.peek())
            v = extractFolder(toks)
            if v == None:
                debugError("Failed attempting to get a Folder. Close items block", toks.peek())
                break
            else:
                items.append(v)
                continue
        
        # clone the dict to avoid polution
        item = dict(((k.lower(), v) for (k, v) in toProp(v[1]).items()))
        item.update({"name": toStr(v[2]), "type": "url"})
        # try to get description
        v = match(toks, [
            (Type.TAG, "DD"),
            (Type.STRING, )
        ])
        if not v == None:
            item["description"] = toStr(v[1])
        else:
            # consuming possible empty description
            v = match(toks, [(Type.TAG, "DD")])
            
        items.append(item)
    
    # test </DL><P> end mark
    v = match(toks, [
        (Type.CLOSETAG, "DL"),
        (Type.TAG, "P")
    ]) or match(toks, [
        (Type.CLOSETAG, "DL")
    ])
    
    if v == None:
        toks.unmark()
        debugError("Error parsing items block ending part ", toks.peek())
        return None
    
    toks.ok()
    return items
    
def extractFolder(toks):
    toks.mark()
    # folder header
    v = match(toks, [
        (Type.TAG, "DT"),
        (Type.TAG, "H3"),
        (Type.STRING, ),
        (Type.CLOSETAG, "H3")
    ])
    
    if v == None:
        toks.unmark()
        debugError("Error parsing folder header ", toks.peek())
        return None
    folder = {"name": toStr(v[2]), "type": "folder"}
    
    # folder description (optional)
    v = match(toks, [
        (Type.TAG, "DD"),
        (Type.STRING, )
    ])
    
    if not v == None:
        folder["description"] = toStr(v[1])
    else:
        # consuming possible empty description
        v = match(toks, [(Type.TAG, "DD")])
    
    v = extractItems(toks)
    if v == None:
        toks.unmark()
        debugError("Error parsing folder items ", toks.peek())
        return None
    folder.update({"children": v})
    
    toks.ok()
    return folder

def test(t, type, name=None):
    """
    Utility function to do token test work
    """
    if t == None:
        return None
    if t[0] == type and (t[0] == Type.STRING or t[1].upper() == name):
        return t
        
def match(toks, pattern):
    r = []
    toks.mark()
    for p in pattern:
        v = toks.next()
        if test(v, *p):
            r.append(v)
        else:
            toks.unmark()
            return None
    
    toks.ok()
    return r

def toStr(t):
    """
    convert string token to string
    """
    return t[1]

def toProp(t):
    """
    convert tag and closeTag token to name and prop tuple
    """
    return t[2]
