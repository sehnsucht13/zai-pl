"""
Module containing the parser class used to produce the AST to be evaluated
by the interpreter.
"""

from yapl.ast_nodes import *
from yapl.tokens import Token, Tok_Type
from yapl.internal_error import InternalSyntaxErr


class Parser:
    """
    Parse and produce an AST from the provided token stream.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_len = len(tokens)
        self.curr_idx = 0
        self.curr_tok = self.tokens[self.curr_idx]

        self.ast = None

    def peek(self, n=1):
        """
        Look ahead and return the Nth token in the token stream. If a numeric
        argument is not provided, return the next token in the stream. If
        there is no next token, return None.
        """
        if self.curr_idx + n < self.tok_len:
            return self.tokens[self.curr_idx + n]
        else:
            return None

    def advance(self, n=1):
        """
        Advance the current token being used by N places. If a numeric
        argument is not provided, return the next token in the stream.
        If there is no next token, return None."""
        if self.curr_idx + n < self.tok_len:
            self.curr_idx += n
            self.curr_tok = self.tokens[self.curr_idx]
            return self.curr_tok
        else:
            return None

    def match(self, token_type, error_str=None):
        """
        Check if the type of the current token being used matches with the provided
        token types. The token types to be checked can be either in a  list or a single
        token.

        There is no error produced from type mismatched yet."""
        assert token_type is not None

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
        error_msg = str()
        if type(token_type) == list:
            error_msg = "Parsing error! Expected either one of {} but got {}".format(
                token_type, self.curr_tok.tok_type
            )
        else:
            error_msg = "Parsing error! Expected {} but got {}".format(
                token_type, self.curr_tok.tok_type
            )
        raise InternalSyntaxErr(error_msg)

    def atom(self):
        """
        Parse an atom(pritive) object.
        Grammar:
        atom := | NUM | STR | ID | BOOL
        ;; Primitives
        BOOL := "false" | "true"
        ID := LETTER (LETTER | NUM | "-" | "$" | "@")*
        NUM := DIGIT (DIGIT)*
        DIGIT := 1 | 2 | 3| 4 | 5 | 6 | 7 | 8 | 9 | 0
        STR := "\"" (LETTER | NUM )* "\""
        """
        if self.curr_tok.tok_type == Tok_Type.ID:
            node = ID_Node(self.curr_tok.literal)
            self.match(Tok_Type.ID)
            return node
        elif self.curr_tok.tok_type == Tok_Type.DQUOTE:
            self.match(Tok_Type.DQUOTE)
            str_token = self.match(Tok_Type.STRING)
            node = String_Node(str_token.literal)
            self.match(Tok_Type.DQUOTE)
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
        """
        Parse a factor rule.
        Grammar:

        factor := "(" expr ")" | unary_op factor | atom
        unary_op := "!" "-"
        """
        # TODO: There will be a problem with the first if statement. Nonetype does not
        # does not have a "tok_type" so it will fail if there is no next token.
        if (
            self.curr_tok.tok_type == Tok_Type.ID
            and self.peek().tok_type == Tok_Type.LROUND
        ):
            func_args = list()
            func_name = self.atom()
            self.match(Tok_Type.LROUND)
            while self.curr_tok.tok_type != Tok_Type.RROUND:
                arg_value = self.or_expr()
                func_args.append(arg_value)
                if self.curr_tok.tok_type != Tok_Type.RROUND:
                    self.match(Tok_Type.COMMA)
            self.match(Tok_Type.RROUND)
            return Func_Call_Node(func_name, func_args)
        elif self.curr_tok.tok_type == Tok_Type.LROUND:
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
        """
        Parse a term rule.
        Grammar:
        term := factor (("*" | "/") factor)*
        """
        left = self.factor()
        while self.curr_tok.tok_type in [Tok_Type.MUL, Tok_Type.DIV]:
            op = self.curr_tok.tok_type
            self.match(op)
            right = self.term()
            left = Arith_Bin_Node(left, op, right)
        return left

    def add_expr(self):
        """
        Parse an addition expression:
        Grammar:
        add_expr := term (("+" | "-") term)*
        """
        left = self.term()
        while self.curr_tok.tok_type in [Tok_Type.PLUS, Tok_Type.MINUS]:
            op = self.curr_tok.tok_type
            self.match(op)
            right = self.term()
            left = Arith_Bin_Node(left, op, right)

        return left

    def rel_expr(self):
        """
        Parse a relative expression:
        Grammar:
        rel_expr := add_expr ( ("<" | ">" | "<=" | ">=") add_expr)*
        """

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
        """
        Parse an equality expression:
        Grammar:
        eq_expr := rel_expr ( ("=="|"!=") rel_expr)*
        """
        left = self.rel_expr()
        while self.curr_tok.tok_type in [Tok_Type.EQ, Tok_Type.NEQ]:
            op = self.curr_tok.tok_type
            self.match(self.curr_tok.tok_type)
            right = self.rel_expr()
            left = Eq_Bin_Node(left, op, right)

        return left

    def and_expr(self):
        """
        Parse an equality expression:
        Grammar:
        eq_expr := rel_expr ( ("=="|"!=") rel_expr)*
        """
        left = self.eq_expr()
        while self.curr_tok.tok_type == Tok_Type.AND:
            op = self.curr_tok.tok_type
            self.match(Tok_Type.AND)
            right = self.eq_expr()
            left = Logic_Bin_Node(left, op, right)

        return left

    def or_expr(self):
        """
        Parse an equality expression:
        Grammar:
        eq_expr := rel_expr ( ("=="|"!=") rel_expr)*
        """
        left = self.and_expr()
        while self.curr_tok.tok_type == Tok_Type.OR:
            op = self.curr_tok.tok_type
            self.match(Tok_Type.OR)
            right = self.and_expr()
            left = Logic_Bin_Node(left, op, right)

        return left

    def expression(self):
        """
        Parse an equality expression:
        Grammar:
        eq_expr := rel_expr ( ("=="|"!=") rel_expr)*
        """
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
        """
        Parse an if statement.
        Grammar:

        if_stmnt := "if" "(" expression ")" statement ( "else" statement )?
        """
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
        """
        Parse a print statement.
        Grammar:

        print := "print" expr
        """
        self.match(Tok_Type.PRINT)
        expr = self.expression()
        self.match(Tok_Type.SEMIC)
        return Print_Node(expr)

    # TODO: Refactor match function and finish parsing functions
    def func_def(self):
        """
        Parse a function definition.
        Grammar:

        func_def := "func" ID "(" ID? ("," ID)* ")" "{" statement* "}"
        """

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
        """
        Parse a block which acts as a nested scope within the program.
        Grammar:

        block := "{" statement* "}"
        """

        self.match(Tok_Type.LCURLY)
        block_stmnts = list()
        while self.curr_tok.tok_type != Tok_Type.RCURLY:
            stmnt = self.statement()
            block_stmnts.append(stmnt)
        self.match(Tok_Type.RCURLY)
        return Block_Node(block_stmnts)

    def simple_expr(self):
        """
        Parse a simple expression.
        Grammar:

        simple_expr := expr ";"
        """
        expr_result = self.expression()
        self.match(Tok_Type.SEMIC)
        return expr_result

    def statement(self):
        """
        Parse a statement.
        Grammar:

        statement := if_stmnt    |
                     while_stmnt | ;; not done
		     for_stmnt   | ;; not done
		     class_def   | ;; not done
		     func_def    |
		     block       |
		     print       |
		     expr
        """
        if self.curr_tok.tok_type == Tok_Type.IF:
            return self.if_statement()
        elif self.curr_tok.tok_type == Tok_Type.FUNC:
            return self.func_def()
        elif self.curr_tok.tok_type == Tok_Type.LCURLY:
            return self.block()
        elif self.curr_tok.tok_type == Tok_Type.PRINT:
            return self.print_statement()
        else:
            return self.simple_expr()

    def program(self):
        """
        Parse a program rule.
        Grammar:
        program := statement*
        """
        prog_node = Program_Node()
        while self.curr_tok.tok_type != Tok_Type.EOF:
            stmnt = self.statement()
            prog_node.add_stmnt(stmnt)
        return prog_node

    def parse(self):
        """
        Parse the provided stream of tokens and return the AST produced.
        """
        ast_root = self.program()
        self.ast = ast_root
        return self.ast
