from abc import abstractclassmethod
class AstTree:
    #TODO:没有添加前驱导致遍历只能递归加上没有使用尾递归之类的。
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
        return self.toString()






