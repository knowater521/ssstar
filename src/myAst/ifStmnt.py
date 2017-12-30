from .AstList import AstList
from io import StringIO
class IfStmnt(AstList):
    def __init__(self,tokens):
        assert len(tokens)>=2 and len(tokens)<=3
        self.hasElse = len(tokens)==3
        super().__init__(tokens)
    def condition(self):
        return self.childrens[0]
    def thenBlock(self):
        return self.childrens[1]
    def elseBlock(self):
        if self.hasElse:
            return self.childrens[2]
        return None
    def toString(self):
        return "(if " + self.condition() + " " + self.thenBlock()\
               + " else " + self.elseBlock() + ")"

