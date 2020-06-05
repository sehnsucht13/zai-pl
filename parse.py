from ast_nodes import *
from lexer import Lexer
from tokens import Token, Tok_Type

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

    def advance(self, n=1):
        if self.curr_idx + n < self.tok_len:
            self.curr_idx += n
            self.curr_tok = self.tokens[self.curr_idx]
            return self.curr_tok
        else:
            return None

    def match(self, tok_type):
        if self.curr_tok.tok_type == tok_type:
            return self.advance(1)
        else:
            # TODO: Create error here
            pass

    def atom(self):
        if self.curr_tok.tok_type == Tok_Type.ID:
            self.match(Tok_Type.ID)
            return ID_Node(self.curr_tok.literal)
        elif self.curr_tok.tok_type == Tok_Type.STRING:
            self.match(Tok_Type.STRING)
            return String_Node(self.curr_tok.literal)
        elif self.curr_tok.tok_type == Tok_Type.NUM:
            self.match(Tok_Type.NUM)
            return Num_Node(self.curr_tok.literal)
        elif self.curr_tok.tok_type == Tok_Type.BOOL:
            self.match(Tok_Type.BOOL)
            return Bool_Node(self.curr_tok.literal)

    def factor(self):
        if self.curr_tok.tok_type == Tok_Type.LRBRACE:
            expr = self.expr()
            match(Tok_Type.RRBRACE)
            return Bracket_Node(expr)
        if self.curr_tok.tok_type in [Tok_Type.BANG, Tok_Type.MINUS]:
            fact = self.factor()
            op = self.curr_tok.tok_type
            match(op)
            return Unary_Node(op, fact)
        else:
            return self.atom()

    def term(self):
        left = self.factor()
        while self.curr_tok.tok_type in [Tok_Type.MUL, Tok_Type.DIV]:
            op = self.curr_tok.tok_type
            self.match(op)
            right = self.term()
            left = Bin_Node(left, op, right)
        return left

    def add_expr(self):
        left = self.term()
        while self.curr_tok.tok_type in [Tok_Type.PLUS, Tok_Type.MINUS]:
            op = self.curr_tok.tok_type
            self.match(op)
            right = self.term()
            left = Bin_Node(left, op, right)

        return left

    def rel_expr(self):
        left = self.add_expr()
        while self.curr_tok.tok_type in [Tok_Type.GT, Tok_Type.GTE, Tok_Type.LT, Tok_Type.LTE]:
            op = self.curr_tok
            self.match(self.curr_tok.tok_type)
            right = self.add_expr()
            left = Bin_Node(left, op, right)

        return left

    def eq_expr(self):
        left = self.rel_expr()
        while self.curr_tok.tok_type in [Tok_Type.EQ, Tok_Type.NEQ]:
            op = self.curr_tok
            self.match(self.curr_tok.tok_type)
            right = self.rel_expr()
            left = Bin_Node(left, op, right)

        return left

    def and_expr(self):
        left = self.eq_expr()
        while self.curr_tok.tok_type == Tok_Type.AND:
            op = self.curr_tok
            self.match(Tok_Type.AND)
            right = self.eq_expr()
            left = Bin_Node(left, op, right)

        return left

    def or_expr(self):
        left = self.and_expr()
        while self.curr_tok.tok_type == Tok_Type.OR:
            op = self.curr_tok
            self.match(Tok_Type.OR)
            right = self.and_expr()
            left = Bin_Node(left, op, right)

        return left

    def expression(self):
       return self.or_expr() 

    def statement(self):
        return self.expression()

    def program(self):
        prog_node = Program_Node()        
        stmnt = self.statement()
        prog_node.add_stmnt(stmnt)
        return prog_node

    def parse(self):
       ast_root = self.program() 
       self.ast = ast_root
       return self.ast

if __name__ == "__main__":
    l = Lexer()
    stream = l.tokenize_string("4 + 4 * 13")
    print("Token stream ", stream)
    p = Parser(stream)
    generated_ast = p.parse()
    print(generated_ast.stmnts)
    

