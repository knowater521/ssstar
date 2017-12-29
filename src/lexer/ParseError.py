class ParseError(Exception):
    def __init__(self,lineno,offSet,line):
        super().__init__("第%s行%s出现了无法解析的单词,第%s列"%(lineno,line,offSet+1))

