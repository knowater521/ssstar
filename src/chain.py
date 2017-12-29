from functools import partial
import string

class Chain:
    def __init__(self,tokenType,*args):
        self.type =tokenType
        self.items=[]
        if len(args)==1:
            self.items.extend(args)
        for each in range(len(args)-1,0,-1):
            nowFn = args[each]
            if each != len(args)-1:
                nextFn = self.items[-1]
            else:
                nextFn=None
            self.items.append(partial(nowFn, nextFn))
        else:
            self.items.append(partial(args[0],self.items[-1]))
        self.items.reverse()
    def __call__(self,rawLine,offSet,*args, **kwargs):
        startFn = self.items[0]
        res= startFn(rawLine, offSet)
        return res

class StringChain(Chain):
    def __init__(self, tokenType, *args):
        super().__init__(tokenType,self.stringStp1,self.stringStp2,self.stringStp3)
    @staticmethod
    def stringStp1(nextFn, line, offSet):
        initalChar = line[offSet]
        if initalChar == '"':
            offSet += 1
            if nextFn:
                while True:
                    res = nextFn(line, offSet)
                    if res == offSet or res >= len(line):
                        offSet = res
                        break
                    else:
                        offSet = res
        return offSet

    @staticmethod
    def stringStp2(nextFn, line, offSet):
        initalChar = line[offSet]
        if initalChar != '"':
            offSet += 1
        elif initalChar == '"':
            res = nextFn(line, offSet)
            offSet = res
        return offSet

    @staticmethod
    def stringStp3(nextFn, line, offSet):
        offSet += 1
        return offSet


class NumberChain(Chain):
    def __init__(self, tokenType, *args):
        super().__init__(tokenType,self.numStp1,self.numStp2)
    @staticmethod
    def numStp1(nextFn, line, offSet):
        initalChar = line[offSet]
        if (string.digits).find(initalChar) != -1:
            offSet += 1
            if nextFn:
                while True:
                    res = nextFn(line, offSet)
                    if res == offSet:
                        break
                    offSet = res
        return offSet

    @staticmethod
    def numStp2(nextFn, line, offSet):
        try:
            initalChar = line[offSet]
        except IndexError:
            return offSet
        if (string.digits).find(initalChar) != -1:
            offSet += 1
            if nextFn:
                while True:
                    res = nextFn(line, offSet)
                    if res == offSet:
                        break
                    offSet = res

        return offSet


binaryOperatorsSingle = ['+', '-', '*', '/', '=', '!', '<',
                             '>', '&', '|']
class OperationChain(Chain):
    def __init__(self, tokenType, *args):
        super().__init__(tokenType,self.operatorStp1,self.operatorStp2)
    @staticmethod
    def operatorStp1(nextFn, line, offSet):
        initalChar = line[offSet]
        opCount = 0
        if initalChar in binaryOperatorsSingle:
            offSet += 1
            opCount += 1
            if nextFn:
                while True:
                    if opCount >= 2:
                        break
                    res = nextFn(line, offSet)
                    if res == offSet or res >= len(line) - 1:
                        offSet = res
                        break
                    else:
                        offSet = res
                        opCount += 1
        return offSet

    @staticmethod
    def operatorStp2(nextFn, line, offSet):
        try:
            initalChar = line[offSet]
        except IndexError:
            return offSet
        if initalChar in binaryOperatorsSingle:
            offSet += 1
            if nextFn:
                while True:
                    res = nextFn(line, offSet)
                    if res == offSet:
                        break
                    offSet = res

        return offSet

class IdentifierChain(Chain):
    def __init__(self, tokenType, *args):
        super().__init__(tokenType,self.idStp1,self.idStp2)
    @staticmethod
    def idStp1(nextFn, line, offSet):
        initalChar = line[offSet]
        if (string.ascii_letters + '_').find(initalChar) != -1:
            offSet += 1
            if nextFn:
                while True:
                    res = nextFn(line, offSet)
                    if res == offSet or res >= len(line):
                        offSet = res
                        break
                    else:
                        offSet = res
        return offSet

    @staticmethod
    def idStp2(nextFn, line, offSet):
        try:
            initalChar = line[offSet]
        except IndexError:
            return offSet
        if (string.ascii_letters + '_' + string.digits).find(initalChar) != -1:
            offSet += 1
            if nextFn:
                while True:
                    res = nextFn(line, offSet)
                    if res == offSet:
                        break
                    offSet = res
        return offSet

separator = ['{','}','(',')','[',']']

class SepartorChain(Chain):
    @staticmethod
    def sepStp(nextFn, line, offSet):
        try:
            initalChar = line[offSet]
        except IndexError:
            return offSet
        if initalChar in separator:
            return offSet+1
        return offSet

    def __init__(self, tokenType, *args):
        super().__init__(tokenType,self.sepStp)

