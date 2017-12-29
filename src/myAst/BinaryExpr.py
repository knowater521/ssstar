from .AstList import AstList

class BinaryExpr(AstList):
    @property
    def operator(self):
        return self.childrens[1].val
    @property
    def left(self):
        return  self.childrens[0].val
    @property
    def right(self):
        return self.childrens[2].val

