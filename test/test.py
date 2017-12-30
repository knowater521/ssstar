from src.lexer.lexer import Lexer
from src.parser.exprParser import ExprParser
from src.tokens import EOF
from src.myAst import *

if __name__ == '__main__':


    file = open('acfun.txt', 'r')
    lexer = Lexer(file)
    ep=ExprParser(lexer)
    aac=ep.expression()
    print(aac.toString())

    # while True:
    #     cc=lexer.read()
    #     print(cc)
    #     if cc == EOF:
    #         break




