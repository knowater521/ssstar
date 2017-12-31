from src.boot import file
from src.tokens import EOF
from src.lexer.lexer import Lexer
from src.parser.opPrecedenceParser import OpPrecedenceParser
import dis
from src.myvm.VirtualMachine import VirtualMachine
from src.code.code import SSCode
if __name__ == '__main__':

    def cc():
        a=10
        b=20
        c=a-b
    # dis.dis(cc)
    # for each in cc.__code__.co_code:
    #     print(each)
    #
    lexer = Lexer(file)
    ep = OpPrecedenceParser(lexer)
    sscode =SSCode(ep.expression())
    vm = VirtualMachine()
    vm.run_code(sscode)




    # while True:
    #     cc=lexer.read()
    #     print(cc)
    #     if cc == EOF:
    #         break



