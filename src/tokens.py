from abc import ABCMeta,abstractclassmethod
from io import StringIO
class Token:
    def __init__(self,lineno,type,val):
        self.type = type
        self.lineno = lineno
        self.val = val

    @property
    def value(self):
        return self.val

    def __str__(self):
        return 'type:%s,lineno:%s,val:%s'%(self.type,self.lineno,self.value)


escapeMap={
    'n':'\n',
    '"':'"',
    '\\':'\\'
}

class StringToken(Token):
    @property
    def value(self):
        res = StringIO()
        stringIter = iter(self.val)
        while True:
            try:
                char=next(stringIter)
                if char=='\\':
                    try:
                        res.write(escapeMap[next(stringIter)])
                    except StopIteration:
                        raise Exception("转义字符位置错误了"+self.val)
                    except KeyError:
                        raise Exception("未实现的转义字符" + self.val)
                else:
                    res.write(char)
            except StopIteration:
                break
        return res.getvalue()
class NumberToken(Token):
    pass
class OperatorToken(Token):
    pass
class SeparatorToken(Token):
    pass
class IdentifierToken(Token):
    pass
class EOL(Token):
    pass

EOF='-1'
