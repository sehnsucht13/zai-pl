from yapl.lexer import Lexer
from yapl.env import Environment, Scope
from yapl.parse import Parser
from yapl.visitor import Visitor


class YAPL_VM:
    """
    Class representing a single instance of the YAPL virtual machine. Each command
    is evaluate within the same context.
    """

    def __init__(self):
        self.env = Environment()
        self.repl_mode_flag = False
        self.visitor = Visitor(self.env)

    def run_repl(self):
        """
        Start a REPL which evaluates every command provided within one VM context.
        """
        self.repl_mode_flag = True
        while True:
            lexer = Lexer()
            str_input = input(">> ")
            tok_stream = lexer.tokenize_string(str_input)
            parser = Parser(tok_stream)
            root = parser.parse()
            val = self.visitor.visit(root)

    def run_string(self, input_str):
        """
        Run a single string within the current VM context.
        """
        lexer = Lexer()
        try:
            tok_stream = lexer.tokenize_string(input_str)
            # print(tok_stream)
            parser = Parser(tok_stream)
            root = parser.parse()
            # print(root)
            val = self.visitor.visit(root)
        except InternalRuntimeErr as e:
            print(e)
