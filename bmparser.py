# -*- coding: utf-8 -*-

from __future__ import print_function

DBGLEN = 20

# type:
#   * String
#   * Tag := (name:String, props:Dict[String, String])
    
class Type:
    STRING = 0
    TAG = 1
    CLOSETAG = 2
    NOTHING = 3
    
    @staticmethod
    def string(str, dbginfo): return (Type.STRING, str, dbginfo)
    
    @staticmethod
    def tag(name, props, dbginfo, isClose=False):
        if isClose:
            return (Type.CLOSETAG, name, props, dbginfo)
        else: 
            return (Type.TAG, name, props, dbginfo)
    
    @staticmethod
    def nothing(dbginfo): return (Type.NOTHING, dbginfo)

class State:
    START = 0
    TAG = 1
    PROPS = 2
    PROP = 3
    QUOTE = 4
    VALUE = 5
    END = 6
    STRING = 7
    NOTHING = 8
    
class ParseException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg
    
    @staticmethod
    def parseError(position, char):
        return ParseException("Invalid char `%s` at %d" % (char, position))
    
    @staticmethod
    def unknownError():
        return ParseException("Unknown parse error")
   
def isValidIDChar(c):
    return c.isalnum() or c == '-' or c == '_'

def readUnit(content, position):
    """
    @return: (nextPosition, type, data)
    """
        
    length = len(content)
    
    state = State.START
    startPosition = position
    tagName = None
    tagProps = {}
    propName = None
    stringVal = None
    isCloseTag = False
    
    while position < length:
        c = content[position]
        
        if state == State.START:
            if c == ' ' or c == '\n':
                pass
            elif c == '<':
                state = State.TAG
                startPosition = position + 1
            else:
                state = State.STRING
                startPosition = position
        elif state == State.TAG:
            if c == ' ':
                state = State.PROPS
                tagName = content[startPosition:position]
            elif isValidIDChar(c):
                pass
            elif c == '!':
                state = State.NOTHING
            elif c == '>':
                state = State.END
                tagName = content[startPosition:position]
                break
            elif c == '/':
                isCloseTag = True
                startPosition = position + 1
            else:
                raise ParseException.parseError(position, c)
        elif state == State.PROPS:
            if c == ' ':
                pass
            elif c == '>':
                state = State.END
                break
            elif isValidIDChar(c):
                state = State.PROP
                startPosition = position
            else:
                raise ParseException.parseError(position, c)
        elif state == State.PROP:
            if c == '=':
                state = State.QUOTE
                propName = content[startPosition:position]
            elif isValidIDChar(c):
                pass
            elif c == ' ':
                state = State.PROPS
                propName = content[startPosition:position]
                tagProps[propName] = propName
            else:
                raise ParseException.parseError(position, c)
        elif state == State.QUOTE:
            if c == '"':
                state = State.VALUE
                startPosition = position + 1
            else:
                raise ParseException.parseError(position, c)
        elif state == State.VALUE:
            if c == '"':
                state = State.PROPS
                tagProps[propName] = content[startPosition:position]
            else:
                pass
        elif state == State.STRING:
            if c == '<':
                stringVal = content[startPosition:position]
                position -= 1
                state = State.END
                break
        elif state == State.NOTHING:
            if c == '>':
                state = State.END
                break
                
        position += 1
    # end while
    dbgstart = max(position - DBGLEN, 0)
    dbgend = min(length, dbgstart + DBGLEN + DBGLEN)
    
    dbginfo = (position, "%s <== %s" % (content[dbgstart:position], content[position:dbgend]))
    
    if state == State.END:
        if tagName:
            return (position + 1, Type.tag(tagName, tagProps, dbginfo, isClose=isCloseTag))
        elif stringVal:
            return (position + 1, Type.string(stringVal, dbginfo))
        else:
            return (position + 1, Type.nothing(dbginfo))
    
    # EOF met and state has not reached END, further processing is needed
    if state == State.STRING:
        stringVal = content[startPosition:]
        return (position, Type.string(stringVal, dbginfo))
        
    if state == State.START:
        return (position, Type.nothing(dbginfo))
    
    # It should be not reachable here
    raise ParseException.unknownError()

def tokenize(content):
    pos = 0
    length = len(content)
    ret = []
    while pos < length:
        (nextPos, result) = readUnit(content, pos)
        pos = nextPos
        if not result[0] == Type.NOTHING:
            ret.append(result)
    return ret
    
def parse(content):
    """
    parse content and return bookmarks as an array
    
    @param content: netscape bookmark content as a string
    @type content: str
    @return: array
    @rtype: array
    """
    pass

