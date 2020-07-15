"""
Module containing the parser class used to produce the AST to be evaluated
by the interpreter.
"""

from yapl.ast_nodes import *
from yapl.tokens import Token, Tok_Type
from yapl.internal_error import InternalParseErr


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

    def match(self, *args):
        """
        Check if the type of the current token being used matches with the provided
        token types. The token types to be checked can be either in a  list or a single
        token.

        There is no error produced from type mismatched yet."""
        if self.curr_tok in args:
            curr_token = self.curr_tok
            self.advance(1)
            return curr_token

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
        if self.curr_tok.tok_type == Tok_Type.THIS:
            node = self.match(Tok_Type.THIS)
            return This_Node()
        elif self.curr_tok.tok_type == Tok_Type.DQUOTE:
            self.match(Tok_Type.DQUOTE)
            str_token = self.match(Tok_Type.STRING)
            node = String_Node(str_token.lexeme)
            self.match(Tok_Type.DQUOTE)
            return node
        elif self.curr_tok.tok_type == Tok_Type.NUM:
            node = self.match(Tok_Type.NUM)
            return Num_Node(node.lexeme)
        elif self.curr_tok.tok_type == Tok_Type.LSQUARE:
            self.match(Tok_Type.LSQUARE)
            array_elem = list()
            while self.curr_tok.tok_type != Tok_Type.RSQUARE:
                arg_value = self.or_expr()
                array_elem.append(arg_value)
                if self.curr_tok.tok_type != Tok_Type.RSQUARE:
                    self.match(Tok_Type.COMMA)
            self.match(Tok_Type.RSQUARE)
            return Array_Node(array_elem)
        elif self.curr_tok.tok_type == Tok_Type.NIL:
            self.match(Tok_Type.NIL)
            return Nil_Node()
        else:
            node = self.match(Tok_Type.TRUE, Tok_Type.FALSE)
            return Bool_Node(node.tok_type)

    def arglist(self):
        func_args = list()
        while self.curr_tok.tok_type != Tok_Type.RROUND:
            arg_value = self.or_expr()
            func_args.append(arg_value)
            if self.curr_tok.tok_type != Tok_Type.RROUND:
                self.match(Tok_Type.COMMA)
        return func_args

    def call_or_access(self):
        if self.peek().tok_type in [
            Tok_Type.LROUND,
            Tok_Type.DOT,
        ]:
            # Create ID node
            node = self.match(Tok_Type.ID)
            left = ID_Node(node.lexeme)

            while self.curr_tok.tok_type in [Tok_Type.LROUND, Tok_Type.DOT]:
                if self.curr_tok.tok_type == Tok_Type.DOT:
                    self.match(Tok_Type.DOT)
                    prop_name = ID_Node(self.match(Tok_Type.ID).lexeme)
                    left = Dot_Bin_Node(left, prop_name)
                elif self.curr_tok.tok_type == Tok_Type.LROUND:
                    self.match(Tok_Type.LROUND)
                    func_args = self.arglist()
                    self.match(Tok_Type.RROUND)
                    left = Call_Node(left, func_args)

            return left
        else:
            node = self.match(Tok_Type.ID)
            return ID_Node(node.lexeme)

    def factor(self):
        """
        Parse a factor rule.
        Grammar:

        factor := "(" expr ")" | unary_op factor | atom
        unary_op := "!" "-"
        """
        # TODO: There will be a problem with the first if statement. Nonetype does not
        # does not have a "tok_type" so it will fail if there is no next token.
        if self.curr_tok.tok_type in [
            Tok_Type.ID,
            Tok_Type.THIS,
        ]:
            return self.call_or_access()
        # Array access
        elif (
            self.curr_tok.tok_type == Tok_Type.ID
            and self.peek().tok_type == Tok_Type.LSQUARE
        ):
            array_name = self.atom()
            self.match(Tok_Type.LSQUARE)
            raw_idx = self.match(Tok_Type.NUM)
            self.match(Tok_Type.RSQUARE)
            array_idx = Num_Node(raw_idx.lexeme)
            return Array_Access_Node(array_name, array_idx)
        elif self.curr_tok.tok_type == Tok_Type.LROUND:
            self.match(Tok_Type.LROUND)
            expr = self.expression()
            self.match(Tok_Type.RROUND)
            return Bracket_Node(expr)
        elif self.curr_tok.tok_type in [Tok_Type.BANG, Tok_Type.MINUS]:
            op = self.match(Tok_Type.BANG, Tok_Type.MINUS)
            fact = self.factor()
            return Unary_Node(op.tok_type, fact)
        # TODO: Handle case of it being an "ID" token instead of just num.
        elif self.curr_tok.tok_type in [Tok_Type.NUM, Tok_Type.ID] and self.peek() in [
            Tok_Type.INCR,
            Tok_Type.DECR,
        ]:
            # Evaluate the initial number token
            node = self.atom()

            # "++" or "--" operators can be nested
            while self.curr_tok.tok_type in [Tok_Type.INCR, Tok_Type.DECR]:
                op = self.match(Tok_Type.INCR, Tok_Type.DECR)
                if op.tok_type == Tok_Type.INCR:
                    node = Incr_Node(node)
                elif op.tok_type == Tok_Type.DECR:
                    node = Decr_Node(node)
            return node
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
            op = self.match(Tok_Type.MUL, Tok_Type.DIV)
            right = self.term()
            left = Arith_Bin_Node(left, op.tok_type, right)

        return left

    def add_expr(self):
        """
        Parse an addition expression:
        Grammar:
        add_expr := term (("+" | "-") term)*
        """
        left = self.term()
        while self.curr_tok.tok_type in [Tok_Type.PLUS, Tok_Type.MINUS]:
            op = self.match(Tok_Type.PLUS, Tok_Type.MINUS)
            right = self.term()
            left = Arith_Bin_Node(left, op.tok_type, right)

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
            op = self.match(Tok_Type.GT, Tok_Type.GTE, Tok_Type.LT, Tok_Type.LTE)
            right = self.add_expr()
            left = Relop_Bin_Node(left, op.tok_type, right)

        return left

    def eq_expr(self):
        """
        Parse an equality expression:
        Grammar:
        eq_expr := rel_expr ( ("=="|"!=") rel_expr)*
        """
        left = self.rel_expr()
        while self.curr_tok.tok_type in [Tok_Type.EQ, Tok_Type.NEQ]:
            op = self.match(Tok_Type.EQ, Tok_Type.NEQ)
            right = self.rel_expr()
            left = Eq_Bin_Node(left, op.tok_type, right)

        return left

    def and_expr(self):
        """
        Parse an equality expression:
        Grammar:
        and_expr := eq_expr ("&&" eq_expr)*
        """
        left = self.eq_expr()
        while self.curr_tok.tok_type == Tok_Type.AND:
            op = self.match((Tok_Type.AND))
            right = self.eq_expr()
            left = Logic_Bin_Node(left, op.tok_type, right)

        return left

    def or_expr(self):
        """
        Parse an equality expression:
        Grammar:
        or_expr := and_expr ("||" and_expr)*
        """
        left = self.and_expr()
        while self.curr_tok.tok_type == Tok_Type.OR:
            op = self.match(Tok_Type.OR)
            right = self.and_expr()
            left = Logic_Bin_Node(left, op.tok_type, right)

        return left

    def expression(self):
        """
        Parse a general expression:
        Grammar:
        expr := "let"? ID "=" or_expr | or_expr
        """
        if self.curr_tok.tok_type == Tok_Type.LET:
            self.match(Tok_Type.LET)
            symbol_path = self.call_or_access()
            self.match(Tok_Type.ASSIGN)
            value = self.or_expr()
            # Check if it is a single node
            if isinstance(symbol_path, ID_Node):
                return New_Assign_Bin_Node(None, symbol_path, value)
            else:
                # Decompose the nodes
                return New_Assign_Bin_Node(symbol_path.left, symbol_path.right, value)
        elif self.curr_tok.tok_type == Tok_Type.ID:
            symbol_path = self.call_or_access()
            if self.curr_tok.tok_type == Tok_Type.ASSIGN:
                self.match(Tok_Type.ASSIGN)
                value = self.expression()
                if isinstance(symbol_path, ID_Node):
                    return Replace_Assign_Bin_Node(None, symbol_path, value)
                else:
                    # Decompose the nodes
                    return Replace_Assign_Bin_Node(
                        symbol_path.left, symbol_path.right, value
                    )
            else:
                # Case of the node not being an assignment node but a simple access
                return symbol_path
        elif self.curr_tok.tok_type == Tok_Type.ID and self.peek().tok_type in [
            Tok_Type.ADDASSIGN,
            Tok_Type.SUBASSIGN,
        ]:
            if self.peek().tok_type == Tok_Type.ADDASSIGN:
                symbol = self.match(Tok_Type.ID).lexeme
                self.match(Tok_Type.ADDASSIGN)
                value = self.or_expr()
                return AddAssign_Node(symbol, value)
            elif self.peek().tok_type == Tok_Type.SUBASSIGN:
                symbol = self.match(Tok_Type.ID).lexeme
                self.match(Tok_Type.SUBASSIGN)
                value = self.or_expr()
                return SubAssign_Node(symbol, value)
        else:
            return self.or_expr()

    def if_statement(self):
        """
        Parse an if statement.
        Grammar:

        if_stmnt := "if" "(" expression ")" statement ( "else" statement )?
        """
        # List used to store all "if condition then" or "elif condition then" pairs.
        conditions = list()

        # Parse "If ... then ..."
        self.match(Tok_Type.IF)
        self.match(Tok_Type.LROUND)
        if_cond = self.or_expr()
        self.match(Tok_Type.RROUND)

        then_block = self.block()
        conditions.append(tuple((if_cond, then_block)))

        # Parse "elif ... then ..."
        while self.curr_tok.tok_type == Tok_Type.ELIF:
            self.match(Tok_Type.ELIF)
            self.match(Tok_Type.LROUND)
            cond = self.or_expr()
            self.match(Tok_Type.RROUND)
            then_block = self.block()
            conditions.append(tuple((cond, then_block)))

        else_block = None
        if self.curr_tok.tok_type == Tok_Type.ELSE:
            self.match(Tok_Type.ELSE)
            else_block = self.block()

        node = If_Node(conditions, else_block)
        return node

    def print_statement(self):
        """
        Parse a print statement.
        Grammar:

        print := "print" expr ";"
        """
        self.match(Tok_Type.PRINT)
        expr = self.or_expr()
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
        func_name = self.match(Tok_Type.ID).lexeme
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
        return Scope_Block_Node(block_stmnts)

    def while_statement(self):
        self.match(Tok_Type.WHILE)
        self.match(Tok_Type.LROUND)
        condition = self.or_expr()
        self.match(Tok_Type.RROUND)

        body = self.block()
        return While_Node(condition, body)

    def switch_stmnt_case(self):
        stmnt_block = list()
        while self.curr_tok.tok_type not in [
            Tok_Type.CASE,
            Tok_Type.DEFAULT,
            Tok_Type.RCURLY,
        ]:
            stmnt = self.statement()
            stmnt_block.append(stmnt)

        # We can reuse the block node to evaluate the statements inside of a switch case.
        # The only difference between the two is how parsing is done. Block nodes require curly brackets
        # while switch case statements do not necessarily require them.
        return Scope_Block_Node(stmnt_block)

    def switch_statement(self):
        self.match(Tok_Type.SWITCH)
        self.match(Tok_Type.LROUND)
        switch_cond = self.or_expr()
        self.match(Tok_Type.RROUND)
        self.match(Tok_Type.LCURLY)

        cases = list()
        while self.curr_tok.tok_type == Tok_Type.CASE:
            self.match(Tok_Type.CASE)
            test_cond = self.or_expr()
            self.match(Tok_Type.COLON)
            block = self.switch_stmnt_case()
            cases.append(tuple((test_cond, block)))

        self.match(Tok_Type.DEFAULT)
        self.match(Tok_Type.COLON)
        default_block = self.switch_stmnt_case()
        self.match(Tok_Type.RCURLY)

        return Switch_Node(switch_cond, cases, default_block)

    def simple_expr(self):
        """
        Parse a simple expression.
        Grammar:

        simple_expr := expr ";"
        """
        expr_result = self.expression()
        self.match(Tok_Type.SEMIC)
        return expr_result

    def class_def(self):
        self.match(Tok_Type.CLASS)
        class_name = self.match(Tok_Type.ID).lexeme
        self.match(Tok_Type.LCURLY)

        class_methods = list()
        while self.curr_tok.tok_type != Tok_Type.RCURLY:
            func_node = self.func_def()
            # Cast regular function node to method node.
            # The parsing procedure is the same for both so there is no point
            # in rewriting the code in a separate parsing procedure.
            method_node = Class_Method_Node(
                func_node.name, func_node.args, func_node.body
            )
            class_methods.append(method_node)

        self.match(Tok_Type.RCURLY)

        return Class_Def_Node(class_name, class_methods)

    def flow_statement(self):
        node = None
        if self.curr_tok.tok_type == Tok_Type.RETURN:
            return_val = None
            self.match(Tok_Type.RETURN)
            # Check if the return statement contains an expression or not.
            if self.curr_tok.tok_type != Tok_Type.SEMIC:
                return_val = self.or_expr()

            node = Return_Node(return_val)
        elif self.curr_tok.tok_type == Tok_Type.BREAK:
            self.match(Tok_Type.BREAK)
            node = Break_Node()
        elif self.curr_tok.tok_type == Tok_Type.CONTINUE:
            self.match(Tok_Type.CONTINUE)
            node = Continue_Node()

        self.match(Tok_Type.SEMIC)
        return node

    def do_while_statement(self):
        self.match(Tok_Type.DO)
        body = self.block()
        self.match(Tok_Type.WHILE)
        self.match(Tok_Type.LROUND)
        test_cond = self.or_expr()
        self.match(Tok_Type.RROUND)
        self.match(Tok_Type.SEMIC)
        return Do_While_Node(test_cond, body)

    def import_statement(self):
        self.match(Tok_Type.IMPORT)
        module_name = self.match(Tok_Type.ID).lexeme
        import_name = None
        if self.curr_tok.tok_type == Tok_Type.AS:
            self.match(Tok_Type.AS)
            import_name = self.match(Tok_Type.ID).lexeme

        return Import_Node(module_name, import_name)

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
        elif self.curr_tok.tok_type == Tok_Type.CLASS:
            return self.class_def()
        elif self.curr_tok.tok_type == Tok_Type.WHILE:
            return self.while_statement()
        elif self.curr_tok.tok_type == Tok_Type.SWITCH:
            return self.switch_statement()
        elif self.curr_tok.tok_type == Tok_Type.LCURLY:
            return self.block()
        elif self.curr_tok.tok_type == Tok_Type.PRINT:
            return self.print_statement()
        elif self.curr_tok.tok_type == Tok_Type.SWITCH:
            return self.switch_statement()
        elif self.curr_tok.tok_type == Tok_Type.DO:
            return self.do_while_statement()
        elif self.curr_tok.tok_type == Tok_Type.IMPORT:
            return self.import_statement()
        elif self.curr_tok.tok_type in [
            Tok_Type.RETURN,
            Tok_Type.CONTINUE,
            Tok_Type.BREAK,
        ]:
            return self.flow_statement()
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
