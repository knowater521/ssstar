from .AstTree import AstTree
from io import StringIO
class AstList(AstTree):

    def __init__(self,tokens):
        # super().__init__(token)
        self.childrens = [].extend(tokens)

    def countOfChildrens(self):
        return len(self.childrens)

    def getChildrenItor(self):
        return self.childrens.__iter__()

    def toString(self):
        sio = StringIO()
        resString = ''
        sio.write('(')
        sep = " "
        for each in self.childrens:
            sio.write(sep)
            sio.write(each.val)
            sio.write(sep)
        sio.write(')')
        return sio.getvalue()

    def location(self):
        return self.childrens[0].lineno
