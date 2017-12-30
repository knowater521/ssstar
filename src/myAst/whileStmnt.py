from .AstList import AstList

class WhileStmnt(AstList):
    def __init__(self,tokens):
        assert len(tokens) == 2
        super().__init__(tokens)
    def condition(self):
        return self.childrens[0]
    def body(self):
        return self.childrens[1]
    def toString(self):
        return "(while " + self.condition() + " " + self.body() + ")"
