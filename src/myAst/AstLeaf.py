from .AstTree import AstTree

class AstLeaf(AstTree):
    def toString(self):
        return self.token.val
    def location(self):
        return self.token.lineno

