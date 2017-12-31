from ..myAst import *

class Precedence:
    def __init__(self,level,isAossRight):
        self.level = level
        self.isAossRight = isAossRight

class OpPrecedenceParser:
    def __init__(self,lexer):
        self.lexer = lexer
        self.operators = dict()
        self.operators['<']=Precedence(1,True)
        self.operators['>']=Precedence(1,True)
        self.operators['+']=Precedence(2,True)
        self.operators['-']=Precedence(2,True)
        self.operators['*']=Precedence(3,True)
        self.operators['/']=Precedence(3,True)
        self.operators['^']=Precedence(4,False)

    def expression(self):
        right = self.factor()
        nextE=None
        while True:
            nextE = self.nextOperator()
            if not nextE:
                break
            right=self.doShift(right,nextE.val)
        return right


    def rightIsExpr(self):
        pass

    def nextOperator(self):
        return False

    def doShift(self,right,next):
        pass

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

