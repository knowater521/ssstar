import inspect
import types
def make_cell(value):
    # Thanks to Alex Gaynor for help with this bit of twistiness.
    # Construct an actual cell object by creating a closure right here,
    # and grabbing the cell object out of the function we create.
    fn = (lambda x: lambda: x)(value)
    return fn.__closure__[0]

class Method:
    def __init__(self, obj, _class, func):
        self.im_self = obj
        self.im_class = _class
        self.im_func = func

    def __repr__(self):  # pragma: no cover
        name = "%s.%s" % (self.im_class.__name__, self.im_func.func_name)
        if self.im_self is not None:
            return '<Bound Method %s of %s>' % (name, self.im_self)
        else:
            return '<Unbound Method %s>' % (name,)
    def __call__(self, *args, **kwargs):
        if self.im_self is not None:
            return self.im_func(self.im_self,args,kwargs)
        else:
            return self.im_func(*args, **kwargs)

class Function:
    __slots__ = [
        'func_code', 'func_name', 'func_defaults', 'func_globals',
        'func_locals', 'func_dict', 'func_closure',
        '__name__', '__dict__', '__doc__',
        '_vm', '_func',
    ]
    def __init__(self,name,code,globals_name,defaults,closure,vm):
        self.func_name=name
        self.func_code=code
        self.func_globals=globals_name
        self.func_defaults=defaults
        self.func_closure=closure
        self._vm=vm
        self.__dict__={}
        self.__doc__ = code.co_consts[0] if code.co_consts else None
        kw = {
            'argdefs': self.func_defaults,
        }
        if closure:
            kw['closure'] = tuple(make_cell(0) for _ in closure)

        self._func = types.FunctionType(code,globals_name)
    def __repr__(self):  # pragma: no cover
        return '<Function %s at 0x%08x>' % (
            self.func_name, id(self)
        )

    def __get__(self, instance, owner):
        if instance is not None:
            return Method(instance, owner, self)
        else:
            return self
    def __call__(self, *args, **kwargs):
        callargs = inspect.getcallargs(self._func, *args, **kwargs)
        frame = self._vm.make_frame(
            self.func_code,self.func_globals,callargs, {}
        )
        CO_GENERATOR = 32
        CO_GENERATOR = 32  # flag for "this code uses yield"
        retval = self._vm.run_frame(frame)
        return retval