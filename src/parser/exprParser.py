from ..myAst import *
from ..tokens import EOF
class ExprParser:
    def __init__(self,lexer):
        self.lexer = lexer

    def expression(self):
        left = self.term()
        while (self.nextIsToken('+') or self.nextIsToken('-')):
            opearator = AstLeaf(self.lexer.read())
            right = self.term()
            left = BinaryExpr([left,opearator,right])
        return left

    def term(self):
        left = self.factor()
        while(self.nextIsToken('*') or self.nextIsToken('/')):
            opearator = AstLeaf(self.lexer.read())
            right = self.factor()
            left = BinaryExpr([left,opearator,right])
        return left

    def factor(self):
        if self.nextIsToken('('):
            self.thisIsToken('(')
            expr = self.expression()
            self.thisIsToken(')')
        else:
            num = self.lexer.read()
            assert num.type == 'Number'
            expr = NumberLiteral(num)
        return expr

    def thisIsToken(self,token):
        thisToken = self.lexer.read()

        assert thisToken.type == 'Separtor'

    def nextIsToken(self,token):
        #事实上就是当前这个而已。
        nextToken = self.lexer.peek(0)[0]
        if nextToken == '-':
            return False

        if nextToken.val == token:
            return True
        return False


