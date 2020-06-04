from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_len = len(tokens)
        self.curr_idx = 0
        self.curr_tok = self.tokens[self.curr_idx]

        self.ast = None

    def peek(self, n=1):
        if self.curr_idx + n < self.tok_len:
            return self.tokens[self.curr_idx + n]
        else:
            return None

    def advance(self, n=1)
        if self.curr_idx + n < self.tok_len:
            self.curr_idx += n
            self.curr_tok = self.tokens[self.curr_idx]
            return self.curr_tok
        else:
            return None

    def match(self, tok_type):
        if self.curr_tok.tok_type == tok_type:
            return self.advance()
        else:
            # TODO: Create error here
            pass

    def parse_expression(self):
        pass

    def parse_statement(self):
        pass

    def parse_program(self):
        pass

    def parse(self):
       ast_root = self.parse_program() 
       self.ast = ast_root
       return self.ast
