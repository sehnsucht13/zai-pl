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

    def match(self, token_type, error_str=None):
        if type(token_type) == list:
            for token in token_type:
                if self.curr_tok.tok_type == token:
                    curr_token = self.curr_tok
                    self.advance(1)
                    return curr_token
        elif self.curr_tok.tok_type == token_type:
            curr_token = self.curr_tok
            self.advance(1)
            return curr_token

        # TODO: Throw error here if there is a mismatch and use error_str to display it.

    def atom(self):
        if self.curr_tok.tok_type == Tok_Type.ID:
            node = ID_Node(self.curr_tok.literal)
            self.match(Tok_Type.ID)
            return node
        elif self.curr_tok.tok_type == Tok_Type.STRING:
            node = String_Node(self.curr_tok.literal)
            self.match(Tok_Type.STRING)
            return node
        elif self.curr_tok.tok_type == Tok_Type.NUM:
            node = Num_Node(self.curr_tok.literal)
            self.match(Tok_Type.NUM)
            return node
        elif self.curr_tok.tok_type in [Tok_Type.TRUE, Tok_Type.FALSE]:
            node = Bool_Node(self.curr_tok.tok_type)
            self.match(self.curr_tok.tok_type)
            return node

    def factor(self):
        if self.curr_tok.tok_type == Tok_Type.LROUND:
            self.match(Tok_Type.LROUND)
            expr = self.expression()
            self.match(Tok_Type.RROUND)
            return Bracket_Node(expr)
        elif self.curr_tok.tok_type in [Tok_Type.BANG, Tok_Type.MINUS]:
            op = self.curr_tok.tok_type
            self.match(op)
            fact = self.factor()
            return Unary_Node(op, fact)
        else:
            return self.atom()

    def term(self):
        left = self.factor()
        while self.curr_tok.tok_type in [Tok_Type.MUL, Tok_Type.DIV]:
            op = self.curr_tok.tok_type
            self.match(op)
            right = self.term()
            left = Arith_Bin_Node(left, op, right)
        return left

    def add_expr(self):
        left = self.term()
        while self.curr_tok.tok_type in [Tok_Type.PLUS, Tok_Type.MINUS]:
            op = self.curr_tok.tok_type
            self.match(op)
            right = self.term()
            left = Arith_Bin_Node(left, op, right)

        return left

    def rel_expr(self):
        left = self.add_expr()
        while self.curr_tok.tok_type in [
            Tok_Type.GT,
            Tok_Type.GTE,
            Tok_Type.LT,
            Tok_Type.LTE,
        ]:
            op = self.curr_tok.tok_type
            self.match(self.curr_tok.tok_type)
            right = self.add_expr()
            left = Relop_Bin_Node(left, op, right)

        return left

    def eq_expr(self):
        left = self.rel_expr()
        while self.curr_tok.tok_type in [Tok_Type.EQ, Tok_Type.NEQ]:
            op = self.curr_tok.tok_type
            self.match(self.curr_tok.tok_type)
            right = self.rel_expr()
            left = Eq_Bin_Node(left, op, right)

        return left

    def and_expr(self):
        left = self.eq_expr()
        while self.curr_tok.tok_type == Tok_Type.AND:
            op = self.curr_tok.tok_type
            self.match(Tok_Type.AND)
            right = self.eq_expr()
            left = Logic_Bin_Node(left, op, right)

        return left

    def or_expr(self):
        left = self.and_expr()
        while self.curr_tok.tok_type == Tok_Type.OR:
            op = self.curr_tok.tok_type
            self.match(Tok_Type.OR)
            right = self.and_expr()
            left = Logic_Bin_Node(left, op, right)

        return left

    def expression(self):
        if (
            self.curr_tok.tok_type == Tok_Type.ID
            and self.peek().tok_type == Tok_Type.ASSIGN
        ):
            symbol = self.curr_tok.literal
            self.match(Tok_Type.ID)
            self.match(Tok_Type.ASSIGN)
            value = self.expression()
            return Assign_Bin_Node(symbol, value)
        else:
            return self.or_expr()

    def if_statement(self):
        self.match(Tok_Type.IF)
        self.match(Tok_Type.LROUND)
        test_expr = self.expression()
        self.match(Tok_Type.RROUND)
        if_stmtn = self.statement()
        else_stmnt = None
        if self.curr_tok.tok_type == Tok_Type.ELSE:
            self.match(Tok_Type.ELSE)
            else_stmnt = self.statement()

        node = If_Node(test_expr, if_stmtn, else_stmnt)
        return node

    def print_statement(self):
        self.match(Tok_Type.PRINT)
        expr = self.expression()
        return Print_Node(expr)

    # TODO: Refactor match function and finish parsing functions
    def func_def(self):
        self.match(Tok_Type.FUNC)
        func_name = self.match(Tok_Type.ID).literal
        self.match(Tok_Type.LROUND)

        # Collect argument symbols for the function
        arg_symbols = list()
        if self.curr_tok.tok_type == Tok_Type.ID:
            func_arg = self.match(Tok_Type.ID)
            arg_symbols.append(func_arg)
            if self.curr_tok.tok_type == Tok_Type.COMMA:
                while self.curr_tok.tok_type != Tok_Type.RROUND:
                    self.match(Tok_Type.COMMA)
                    func_arg = self.match(Tok_Type.ID)
                    arg_symbols.append(func_arg)

        self.match(Tok_Type.RROUND)
        self.match(Tok_Type.LCURLY)

        func_body = list()
        while self.curr_tok.tok_type != Tok_Type.RCURLY:
            func_stmnt = self.statement()
            func_body.append(func_stmnt)
        self.match(Tok_Type.RCURLY)

        return Func_Node(func_name, arg_symbols, func_body)

    def block(self):
        self.match(Tok_Type.LCURLY)
        block_stmnts = list()
        while self.curr_tok.tok_type != Tok_Type.RCURLY:
            stmnt = self.statement()
            block_stmnts.append(stmnt)
        self.match(Tok_Type.RCURLY)
        return Block_Node(block_stmnts)

    def statement(self):
        # print("Statement ", self.curr_tok)
        if self.curr_tok.tok_type == Tok_Type.IF:
            return self.if_statement()
        elif self.curr_tok.tok_type == Tok_Type.FUNC:
            return self.func_def()
        elif self.curr_tok.tok_type == Tok_Type.LCURLY:
            return self.block()
        elif self.curr_tok.tok_type == Tok_Type.PRINT:
            return self.print_statement()
        else:
            return self.expression()

    def program(self):
        prog_node = Program_Node()
        while self.curr_tok.tok_type != Tok_Type.EOF:
            stmnt = self.statement()
            prog_node.add_stmnt(stmnt)
        return prog_node

    def parse(self):
        ast_root = self.program()
        self.ast = ast_root
        return self.ast


# if __name__ == "__main__":
#     l = Lexer()
#     stream = l.tokenize_string("4 + 4 * 13")
#     print("Token stream ", stream)
#     p = Parser(stream)
#     generated_ast = p.parse()
#     print(generated_ast.stmnts)
