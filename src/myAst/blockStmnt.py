from .AstList import AstList

class BlockStmnt(AstList):
    def __init__(self,tokens):
        super().__init__(tokens)
    def toString(self):
        pass