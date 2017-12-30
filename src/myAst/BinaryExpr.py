from .AstList import AstList

class BinaryExpr(AstList):
    # def __init__(self,*args):
    #     super().__init__(*args)
    def operator(self):
        return self.childrens[1].val
    @property
    def left(self):
        return self.childrens[0].val
    @property
    def right(self):
        return self.childrens[2].val

