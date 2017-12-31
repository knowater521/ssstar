from src.tokens import *
from .ParseError import ParseError
from ..chain import *


tokenMap ={
    'String':StringToken,
    'Number':NumberToken,
    'Operator':OperatorToken,
    'Identifier':IdentifierToken,
    'Separtor':SeparatorToken,
}

class Lexer:
    #TODO:事实证明,offset不对，应该穿字符串过去才对的。下次改过来才行了。
    @staticmethod
    def linebreak(line,offSet):
        if(line[offSet]=='\n'):
            return offSet+1
        return offSet

    def raiseErro(self,*args):
        raise ParseError(lineno=self.currLineno,offSet=args[1],line=args[0])

    def __init__(self,file):
        self.file = file
        self.tokenList = []
        self.hasMore = True
        self.composeChain()
        self.currLineno=0

    def composeChain(self):
        self.strChain = StringChain('String')
        self.numChain = NumberChain('Number')
        self.operatorChain = OperationChain('Operator')
        self.idChain = IdentifierChain('Identifier')
        self.sepChain = SepartorChain('Separtor')
        self.strategies = [self.idChain,self.numChain,
                           self.strChain,self.operatorChain,
                           self.sepChain,self.linebreak,
                           self.raiseErro]
        self.strategies.append(self.raiseErro)
    def peek(self,count:int):
        if(self.addIntoTokenList(count)):
            return self.tokenList[0:1]
        else:
            return EOF

    def read(self):
        if(self.addIntoTokenList(0)):
            return self.tokenList.pop(0)
        else:
            return EOF

    def addIntoTokenList(self,i:int):
        while(i>=len(self.tokenList)):
            if self.hasMore:
                self.handleAline()
            else:
                return False
        return True

    def handleAline(self):
        self.currLineno +=1
        newLine = self.file.readline()
        if(newLine is ''):
            self.hasMore=False
            return
        elif newLine == '\n':
            return
        offSet = 0
        while True:
            if offSet > len(newLine)-1:
                break
            if (newLine[offSet-1+1] == ' '):
                offSet += 1
                continue
            offSet = self.tryEveryStrategies(newLine,offSet)
            if newLine[offSet-1] == '\n' or offSet==len(newLine):
                break

    def tryEveryStrategies(self, line, offSet):
        for each in self.strategies:
            res = each(line, offSet)
            if res == offSet:
                assert type(res)==int
                continue
            else:
                if line[offSet:res] == '\n':
                    pass
                else:
                    tokenVal = line[offSet:res]
                    tokenType=each.type
                    tokenLineno = self.currLineno
                    tokenClass = tokenMap[tokenType]
                    # print(tokenType)
                    self.tokenList.append(tokenClass(tokenLineno,tokenType,tokenVal))
                return res
