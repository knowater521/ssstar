from functools import partial
# from .lexer.lexer import Lexer
import string

def handleEscape(file,line ,offSet=0):
    nextChar = line[offSet]
    if nextChar == '"'  or nextChar=='\\':
        offSet+=1
        return offSet
    return offSet



file = open('acfun.txt', 'r')
handleEscapecc = partial(handleEscape,file)
