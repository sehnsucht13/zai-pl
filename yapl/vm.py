"""Module contains a class used to manage the entire virtual machine."""
from yapl.lexer import Lexer
from yapl.env import Environment
from yapl.parse import Parser
from yapl.visitor import Visitor
from yapl.internal_error import (
    InternalRuntimeErr,
    InternalTypeError,
    InternalTokenErr,
    InternalParseErr,
)

import atexit
import os
import readline


class YAPL_VM:
    """
    Class representing a single instance of the YAPL virtual machine. Each command
    is evaluate within the same context.
    """

    def __init__(self):
        self.env = Environment()
        self.repl_mode_flag = False
        self.visitor = Visitor(self.env)
        self.__load_stdlib()

    def __load_stdlib(self):
        """Load both the standard library in the environment of the current VM instance."""
        from yapl.stdlib.native_func import register_functions

        native_functions = register_functions()
        curr_scope = self.env.peek()
        for func in native_functions:
            curr_scope.new_variable(func.name, func)

    def __setup_readline(self):
        histfile = os.path.join(os.path.expanduser("~"), ".yapl_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(2000)
        except FileNotFoundError:
            pass

        atexit.register(readline.write_history_file, histfile)

    def run_repl(self):
        """
        Start a REPL which evaluates every command provided within one VM context.
        """
        self.repl_mode_flag = True
        self.__load_stdlib()
        self.__setup_readline()
        while True:
            lexer = Lexer()
            try:
                str_input = input(">> ")
                tok_stream = lexer.tokenize_string(str_input)
                parser = Parser(tok_stream, str_input)
                root = parser.parse()
                val = self.visitor.visit(root)
                if val is not None:
                    print(str(val))
            except InternalRuntimeErr as e:
                print(e)
            except InternalTypeError as e:
                print(e)
            except InternalTokenErr as e:
                print(e)
            except InternalParseErr as e:
                print(e)

    def run_string(self, input_str):
        """
        Run a single string within the current VM context.
        """
        self.__load_stdlib()
        lexer = Lexer()
        try:
            tok_stream = lexer.tokenize_string(input_str)
            parser = Parser(tok_stream, input_str)
            root = parser.parse()
            val = self.visitor.visit(root)
        except InternalRuntimeErr as e:
            print(e)
        except InternalTypeError as e:
            print(e)
        except InternalTokenErr as e:
            print(e)
        except InternalParseErr as e:
            print(e)
