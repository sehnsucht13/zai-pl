# Copyright 2021 by Yavor Konstantinov <ykonstantinov1@gmail.com>

# This file is part of zai-pl.

# zai-pl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# zai-pl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with zai-pl. If not, see <https://www.gnu.org/licenses/>.

"""Module contains a class used to manage the entire virtual machine."""
from zai.lexer import Lexer
from zai.env import Environment
from zai.parse import Parser
from zai.visitor import Visitor
from zai.internal_error import (
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
        self.current_completions = None

    def __load_stdlib(self):
        """
        Load both the standard library in the environment of the current VM instance.
        """
        from zai.stdlib.native_func import register_functions

        native_functions = register_functions()
        curr_scope = self.env.peek()
        for func in native_functions:
            curr_scope.new_variable(func.name, func)

    # def __complete(self, text, state):
    #     if state == 0:
    #         print("Text from complete", text)
    #         new_completions = list()
    #         curr_scope = self.env.peek()
    #         print(curr_scope.keys())
    #     elif state < len(a):
    #         return a[state]
    #     else:
    #         return None

    def __setup_readline(self):
        histfile = os.path.join(os.path.expanduser("~"), ".zai_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(2000)
        except FileNotFoundError:
            pass

        atexit.register(readline.write_history_file, histfile)

        # # Set up autocompletion with "TAB" key
        # readline.parse_and_bind("tab: complete")
        # readline.set_completer(self.__complete)

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
            self.visitor.visit(root)
        except InternalRuntimeErr as e:
            print(e)
        except InternalTypeError as e:
            print(e)
        except InternalTokenErr as e:
            print(e)
        except InternalParseErr as e:
            print(e)
