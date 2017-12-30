from src.lexer.lexer import Lexer
from src.parser.exprParser import ExprParser
from src.tokens import EOF
from src.myAst import *

if __name__ == '__main__':
    # ep=ExprParser(lexer)
    # aac=ep.expression()
    # print(aac.toString())
    file = open('acfun.txt', 'r')
    lexer = Lexer(file)

    while True:
        cc=lexer.read()
        print(cc)
        if cc == EOF:
            break

