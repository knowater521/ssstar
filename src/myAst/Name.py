from .AstLeaf import AstLeaf

class Name(AstLeaf):
    @property
    def name(self):
        return self.token.val