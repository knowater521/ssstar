import collections
class FakedFrame:
    def __init__(self):
        self.cells=None
class Frame:
    def __init__(self,code,globals_name,locals_name,f_back):
        self.code_obj=code
        self.globals_name=globals_name
        self.locals_name=locals_name
        self.stack=[]
        self.block_stack=[]
        self.f_lineno = self.code_obj.co_firstlineno
        self.offset=0
        self.f_back=f_back
        if f_back:
            self.f_builtins = f_back.f_builtins
        else:
            self.f_builtins = locals_name['__builtins__']
            f_back= FakedFrame()
            if hasattr(self.f_builtins, '__dict__'):
                self.f_builtins = self.f_builtins.__dict__
        if code.co_cellvars:
            self.cells={}

            if f_back and not f_back.cells:
                f_back.cells = {}

            '前一个帧和现在的帧都有一个Cell的引用。可以进行一起修改。'
            for var in code.co_cellvars:
                cell = Cell(self.locals_name.get(var))
                f_back.cells[var] = self.cells[var] = cell
        else:
            self.cells=None
        if code.co_freevars:
            pass
    def __repr__(self):  # pragma: no cover
        return '<Frame at 0x%08x: %r @ %d>' % (
            id(self), self.code_obj.co_filename, self.f_lineno
        )

    def line_number(self):
        lnotab = self.code_obj.co_lnotab

Block = collections.namedtuple("Block", "type, handler, level")
class Cell:
    def __init__(self, value):
        self.contents = value

    def get(self):
        return self.contents

    def set(self, value):
        self.contents = value