from .AstLeaf import AstLeaf

class Name(AstLeaf):
    @property
    def val(self):
        return self.token.val
    # def val