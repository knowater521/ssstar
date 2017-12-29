from src.lexer.lexer import Lexer
from src.tokens import EOF
from abc import ABCMeta,abstractclassmethod,abstractproperty
import sys

from src.myAst import *
if __name__ == '__main__':

    file = open('acfun.txt', 'r')
    lexer = Lexer(file)
    while True:
        cc=lexer.read()
        print(cc)
        if cc == EOF:
            break




