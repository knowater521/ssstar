from .AstTree import AstTree
from io import StringIO
class AstList(AstTree):

    def __init__(self,tokens):
        # super().__init__(token)
        self.childrens = tokens
    def countOfChildrens(self):
        return len(self.childrens)

    def getChildrenItor(self):
        return self.childrens.__iter__()

    def toString(self):
        sio = StringIO()
        sio.write('(')
        sep = " "
        for each in self.childrens:
            sio.write(sep)
            #每一个不同的class没有实现同样的接口就麻烦了，不统一啊。
            sio.write(each.toString())
            sio.write(sep)
        sio.write(')')
        return sio.getvalue()

    def location(self):
        return self.childrens[0].lineno
