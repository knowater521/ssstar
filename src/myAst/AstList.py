from .AstTree import AstTree

class AstList(AstTree):

    def __init__(self,tokens):
        # super().__init__(token)
        self.childrens = [].extend(tokens)

    def countOfChildrens(self):
        return len(self.childrens)

    def getChildrenItor(self):
        return self.childrens.__iter__()

    def toString(self):
        resString = ''
        resString += '('
        sep = " "
        for each in self.childrens:
            resString+=sep
            resString+=each.val
            resString+=sep
        resString+=')'
        return resString

    def location(self):
        return self.childrens[0].lineno
