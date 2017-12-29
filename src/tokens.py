from abc import ABCMeta,abstractclassmethod
class Token:
    def __init__(self,lineno,type,val):
        self.type = type
        self.lineno = lineno
        self.val = val

    def __str__(self):
        return 'type:%s,lineno:%s,val:%s'%(self.type,self.lineno,self.val)

class StringToken(Token):
    pass
class NumberToken(Token):
    pass
class OperatorToken(Token):
    pass
class SeparatorToken(Token):
    pass
class IdentifierToken(Token):
    pass
class EOL(Token):
    pass

EOF='-1'
