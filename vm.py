from lexer import Lexer
from parse import Parser
from visitor import Visitor


def main():
    while True:
        lexer = Lexer()
        str_input = input(">> ")
        tok_stream = lexer.tokenize_string(str_input)
        parser = Parser(tok_stream)
        root = parser.parse()
        # print(str_input)
        print(tok_stream)
        v = Visitor()
        val = v.visit(root)
        # print(val)


if __name__ == "__main__":
    main()
