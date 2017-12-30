from abc import abstractclassmethod
class AstTree:
    def __init__(self,token):
        self.token=token
        self.lineno = token.lineno
    @abstractclassmethod
    def location(self):
        return ''
    @abstractclassmethod
    def toString(self):
        return ''
    @abstractclassmethod
    def countOfChildrens(self):
        pass
    @abstractclassmethod
    def getChildrenItor(self):
        pass
    @abstractclassmethod
    def toString(self):
        pass
    def __str__(self):
        return self.toString






