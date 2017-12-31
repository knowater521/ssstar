from .AstList import AstList
class BinaryExpr(AstList):
    def __init__(self,*args):
        super().__init__(*args)
        # self.op=args[1]
    def operator(self):
        return self.childrens[1]
    @property
    def left(self):
        return self.childrens[0]
    @property
    def right(self):
        return self.childrens[2]
