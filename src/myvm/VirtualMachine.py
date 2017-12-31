import builtins
import dis
import operator
import traceback

from .Frame import Frame, Block
from .Function import Function
from .VirtualMachineException import VirtualMachineException


class VirtualMachine:
    def __init__(self):

        self.offset=0
        self.frame=None
        self.frames = []
    def parse_byte_and_args(self):
        frame = self.frame
        frame_code_obj=frame.code_obj
        code = frame_code_obj.co_code[self.offset]
        name = dis.opname[code]

        arg=None
        if code >=dis.HAVE_ARGUMENT:
            #解释一下这里，和汇编语言非常类似的，参数由一个字组成，前面的为第8位后面为高8位，它们组成了一个16位的参数，你也可以用位运算实现。
            offsetOfArg=frame_code_obj.co_code[self.offset+1]+(frame_code_obj.co_code[self.offset+2]*2**8)
            if code in dis.hasname:
                arg = frame_code_obj.co_names[offsetOfArg]
            elif code in dis.hasconst:
                arg = frame_code_obj.co_consts[offsetOfArg]
            elif code in dis.haslocal:
                arg = frame_code_obj.co_varnames[offsetOfArg]
            elif code in dis.hasjrel:
                arg = offsetOfArg + self.offset + 3
            elif code in dis.cmp_op:
                arg = offsetOfArg
            elif code in dis.hasfree:
                arg = frame_code_obj.co_cellvars[offsetOfArg]
            else:
                arg = offsetOfArg
            self.offset+=3
        else:
            self.offset+=1
        return name,arg

    def run_code(self,code,global_names=None, local_names=None):

        frame = self.make_frame(code,global_names,local_names,self.frame)
        ret_val=self.run_frame(frame)
        if self.frames:
            raise VirtualMachineException("Frames left over!")
        elif self.frame and self.frame.stack:
            raise VirtualMachineException("Data left on stack! %r" % self.frame.stack)


    def make_frame(self,code,f_globals=None,f_locals=None,before_frame=None):
        f_globals=f_locals={
            "__builtins__":builtins,
            "__name__":"__main__",
            "__doc__":None,
            "__package__":None
        }
        frame = Frame(code,f_globals,f_locals,self.frame)
        return frame

    def run_frame(self,frame):

        self.push_frame(frame)
        while True:
            byte_name,arg=self.parse_byte_and_args()
            # print(byte_name,arg)
            if byte_name == "RETURN_VALUE":
                self.dispatch(byte_name, arg)
                break
            why=self.dispatch(byte_name, arg)
            if why == 'exception':
                traceback.print_exc()
        self.pop_frame()
    def push(self,val):
        assert self.frame is not None
        try:
            self.frame.stack.append(val)
        except:

            print(self.frames)
            print(self.frame)
            exit(1)
    def pop(self,index=0):
        # print(self.frames)
        return self.frame.stack.pop(-1-index)
    def top(self):
        return self.frame.stack[-1]
    def jump(self,where):
        self.offset=where
    def push_frame(self,frame):
        if self.frame:
            self.frame.offset = self.offset
            self.offset = frame.offset
        self.frame = frame
        self.frames.append(frame)
    def push_block(self,type,handler=None,level=None):
        if level is None:
            level = len(self.frame.stack)
        self.frame.block_stack.append(Block(type,handler,level))
    def pop_frame(self):
        self.frames.pop()
        if self.frames:

            frame = self.frames.pop()

            self.offset = frame.offset
            self.run_frame(frame)
        else:
            self.frame = None

    def pop_block(self):
        return self.frame.block_stack.pop()
    def popn(self, n):
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []
    def byte_JUMP_ABSOLUTE(self, jump):
        self.jump(jump)
    def byte_RETURN_VALUE(self):
        val = self.pop()
        # print(val)
        if self.frame.f_back:
            self.frame.f_back.stack.append(val)
        else:
            pass

    def dispatch(self,byte_name, argument):
        why = None

        try:
            if byte_name.startswith('BINARY_'):
                self.binaryOperator(byte_name[7:])
            elif byte_name.startswith('INPLACE_'):
                pass
            else:
                bytecode_fn = getattr(self, 'byte_%s'%byte_name, None)

                if bytecode_fn == None:
                    raise Exception('aa')
                if argument is None and byte_name is not "LOAD_CONST":
                    why = bytecode_fn()
                else:
                    why = bytecode_fn(argument)
        except Exception as e:
            traceback.print_exc()
            exit(1)
            why='exception'
        return why


    def byte_STORE_FAST(self,name):
        val = self.pop()
        self.frame.locals_name[name]=val
    def byte_LOAD_FAST(self,name):
        try:
            val = self.frame.locals_name[name]
        except:
            traceback.print_exc()
            raise KeyError("找不到这个%s"%name)
        self.push(val)

    def byte_LOAD_CONST(self,const):
        self.push(const)
    def byte_LOAD_GLOBAL(self,global_name):
        #global暂时只可以使用內建的函数。
        try:
            val = builtins.__dict__[global_name]
        except:
            raise NameError("global name '%s' is not defined" % global_name)
        self.push(val)
    def byte_CALL_FUNCTION(self,arg):
        self.call_function(arg,[],{})
    def byte_MAKE_FUNCTION(self,arg):
        name = self.pop()
        code = self.pop()
        f_globals = self.frame.globals_name
        defaults = self.popn(arg)
        fn = Function(name,code,f_globals,defaults,None,self)
        self.push(fn)

    def byte_BUILD_LIST(self,countOfargs):
        args=self.popn(countOfargs)
        self.push(args)
    def byte_SETUP_LOOP(self,dest):
        self.push_block('loop',dest)
    def byte_POP_BLOCK(self):
        self.pop_block()
    def call_function(self,arg,args,kwargs):
        lenKw, lenPos = divmod(arg, 256)
        namedargs = {}
        for i in range(lenKw):
            key, val = self.popn(2)
            namedargs[key] = val
        namedargs.update(kwargs)
        posargs = self.popn(lenPos)
        posargs.extend(args)
        func = self.pop()
        frame = self.frame
        if hasattr(func, 'im_func'):
            # Methods get self as an implicit first parameter.
            if func.im_self:
                posargs.insert(0, func.im_self)
            # The first parameter must be the correct type.
            if not isinstance(posargs[0], func.im_class):
                raise TypeError(
                    'unbound method %s() must be called with %s instance '
                    'as first argument (got %s instance instead)' % (
                        func.im_func.func_name,
                        func.im_class.__name__,
                        type(posargs[0]).__name__,
                    )
                )
            func = func.im_func
        retval = func(*posargs, **namedargs)

        self.push(retval)
    def byte_GET_ITER(self):
        val =self.pop()
        self.push(iter(val))
    def byte_STORE_DEREF(self,name):
        print()
        self.frame.cells[name].set(self.pop())
    def byte_LOAD_CLOSURE(self,name):
        self.push(self.frame.cells[name])
    def byte_BUILD_TUPLE(self,arg):

        vals = self.popn(arg)
        myTuple=tuple(vals)

        self.push(myTuple)

    def byte_MAKE_CLOSURE(self, argc):
        name = self.pop()
        closure, code = self.popn(2)
        defaults = self.popn(argc)
        print(closure)
        globs = self.frame.globals_name
        fn = Function(name, code, globs, defaults, closure, self)
        self.push(fn)
    def byte_FOR_ITER(self,jump):
        argIter = self.top()
        try:
            val = argIter.__next__()
            self.push(val)
        except StopIteration:
            self.pop()
            self.jump(jump)
            # traceback.print_exc()
            # exit(1)
    def byte_POP_TOP(self):
        self.pop()
    def byte_POP_JUMP_IF_FALSE(self,where):
        val = self.pop()
        if (not val):
            self.jump(where=where)

    def binaryOperator(self,name):
        x, y = self.popn(2)
        self.push(self.BINARY_OPERATORS[name](x, y))
    BINARY_OPERATORS ={
        "ADD":operator.add,
        "SUBTRACT":operator.sub,
        "MULTIPLY":operator.mul,
        "TRUE_DIVIDE":operator.itruediv,
    }
    def byte_COMPARE_OP(self,op):
        x,y =self.popn(2)
        val=self.COMPARE_OPERATORS[op](x,y)
        self.push(val)
    COMPARE_OPERATORS = [
        operator.lt,
        operator.le,
        operator.eq,
        operator.ne,
        operator.gt,
        operator.ge,
    ]

