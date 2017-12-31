from ..myAst import *
from ..tokens import *

class Precedence:
    def __init__(self,level,leftAssoc):
        self.level = level
        self.leftAssoc = leftAssoc

class OpPrecedenceParser:
    def __init__(self,lexer):
        self.lexer = lexer
        self.operators = dict()
        self.operators['='] = Precedence(0, True)
        self.operators['<'] = Precedence(1, True)
        self.operators['>'] = Precedence(1, True)
        self.operators['+'] = Precedence(2, True)
        self.operators['-'] = Precedence(2, True)
        self.operators['*'] = Precedence(3, True)
        self.operators['/'] = Precedence(3, True)
        self.operators['^'] = Precedence(4, False)

    def expression(self):
        right = self.factor()
        nextOp=None
        while True:
            nextOp = self.nextOperator()
            if not nextOp:
                break
            right=self.doShift(right,nextOp)
        return right


    def rightIsExpr(self,prevOp,nextOp):
        if (nextOp.leftAssoc):
            return prevOp.level < nextOp.level
        else:
            return prevOp.level <= nextOp.level

    def nextOperator(self):
        nextOp = self.lexer.peek(0)[0]
        if nextOp == '-':
            return False
        if (nextOp.type == 'Operator'):
            return  self.operators[nextOp.value]
        else:
            return False

    def doShift(self,left,prevOp):
        op = self.lexer.read()
        right = self.factor()
        nextOp=None
        while True:
            nextOp=self.nextOperator()
            if nextOp  and self.rightIsExpr(prevOp,nextOp):
                right=self.doShift(right,nextOp)
            return BinaryExpr([left,op,right])



    def factor(self):
        if self.nextIsToken('('):
            self.thisIsToken('(')
            expr = self.expression()
            self.thisIsToken(')')
        else:
            num = self.lexer.read()
            assert num.type == 'Number' or num.type == 'Identifier'
            if num.type == 'Number':
                expr = NumberLiteral(num)
            else:
                expr = Name(num)


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

