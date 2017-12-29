from .AstLeaf import AstLeaf

class NumberLiteral(AstLeaf):
    @property
    def val(self):
        return self.token.val

