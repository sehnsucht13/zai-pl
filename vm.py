from lexer import Lexer
from parse import Parser
from visitor import Visitor


def main():
    v = Visitor()
    while True:
        lexer = Lexer()
        str_input = input(">> ")
        tok_stream = lexer.tokenize_string(str_input)
        # print(tok_stream)
        parser = Parser(tok_stream)
        root = parser.parse()
        val = v.visit(root)


if __name__ == "__main__":
    main()
