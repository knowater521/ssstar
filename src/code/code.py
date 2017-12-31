import dis

from src.myAst import *

class SSCode:
    def __init__(self,astTree):
        self.co_code = []
        self.co_consts = [None]
        self.co_varnames = []
        self.co_firstlineno=1
        self.co_cellvars=None
        self.co_freevars=None
        self.mapping={
            '+':'add',
            '-':'sub',
            '*':'mul',
            '/':'div',
            '=':'eq'
        }
        self.astTree=astTree
        self.acfun(astTree)
        self.appendRtn()

        # print(self.co_varnames,self.co_consts)
        # for each in self.co_code:
        #
        #     print(dis.opname[each],each)
    def appendRtn(self):
        opcode = dis.opmap['LOAD_CONST']
        self.co_code.append(opcode)
        self.co_code.append(0)
        self.co_code.append(0)
        opcode = dis.opmap['RETURN_VALUE']
        self.co_code.append(opcode)
    def add(self,arg):
        opcode = dis.opmap['BINARY_ADD']
        self.co_code.append(opcode)

    def sub(self,arg):
        opcode = dis.opmap['BINARY_SUBTRACT']
        self.co_code.append(opcode)

    def eq(self,arg):
        opcode = dis.opmap['STORE_FAST']
        self.co_code.append(opcode)
        self.co_code.append(arg)
        self.co_code.append(0)

    def addInFrame(self,val):
        if type(val) == Name:
            if val not in self.co_varnames:
                self.co_varnames.append(val.val)
                return len(self.co_varnames)-1
        elif type(val) == NumberLiteral:
            if val not in self.co_consts:
                self.co_consts.append(val.val)
                opcode = dis.opmap['LOAD_CONST']
                self.co_code.append(opcode)
                pos = len(self.co_consts)-1
                self.co_code.append(pos)
                self.co_code.append(0)
        else:
            print(val)
            raise Exception("奇怪的变量无法储存")
    def acfun(self,node):
        if type(node) != BinaryExpr:
            return

        if node.right:
            self.acfun(node.right)

        if node.left:
            self.acfun(node.left)

        if node.operator:
            if isinstance(node.right,AstLeaf):
                # rightArg = node.right.toString()
                arg=self.addInFrame(node.right)
            if isinstance(node.left,AstLeaf):
                # leftArg = node.left.toString()
                arg=self.addInFrame(node.left)

            op = node.operator().value
            method = getattr(self,self.mapping[op])
            method(arg)
        return

