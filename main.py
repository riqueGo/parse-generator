from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser
from ArithmeticVisitor import ArithmeticVisitor


def main():
    visitor = ArithmeticVisitor()
    while True:
        expression = input(">> ")
        lexer = ArithmeticLexer(InputStream(expression))
        stream = CommonTokenStream(lexer)
        parser = ArithmeticParser(stream)
        tree = parser.program()
        result = visitor.visit(tree)
        if result:
            print(str(result))

if __name__ == '__main__':
    main()