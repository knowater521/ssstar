from src.boot import file
from src.tokens import EOF
from src.myAst import *
from io import StringIO
from src.lexer.lexer import Lexer
if __name__ == '__main__':
    # ep=ExprParser(lexer)
    # aac=ep.expression()
    # print(aac.toString())
    # asdas = 'a'




    lexer = Lexer(file)
    while True:
        cc=lexer.read()
        print(cc)
        if cc == EOF:
            break

