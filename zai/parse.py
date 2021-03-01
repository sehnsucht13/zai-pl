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

"""
Module containing the parser class used to produce the AST to be evaluated
by the interpreter.
"""

from zai.ast_nodes import (
    This_Node,
    String_Node,
    Num_Node,
    Array_Node,
    Array_Access_Node,
    Nil_Node,
    Bool_Node,
    Arith_Bin_Node,
    ID_Node,
    Dot_Bin_Node,
    Bracket_Node,
    Unary_Node,
    Incr_Node,
    Decr_Node,
    Call_Node,
    AddAssign_Node,
    SubAssign_Node,
    New_Assign_Bin_Node,
    If_Node,
    Print_Node,
    Func_Node,
    Scope_Block_Node,
    While_Node,
    Break_Node,
    Continue_Node,
    Do_While_Node,
    Import_Node,
    Program_Node,
    Switch_Node,
    Class_Def_Node,
    Class_Method_Node,
    Return_Node,
    Replace_Assign_Bin_Node,
    Relop_Bin_Node,
    Eq_Bin_Node,
    Logic_Bin_Node,
)
from zai.tokens import Tok_Type
from zai.internal_error import InternalParseErr


class Parser:
    """
    Parse and produce an AST from the provided token stream.
    """

    def __init__(self, tokens, original_text):
        self.original_text = original_text
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
        else:
            raise InternalParseErr(
                self.curr_tok.line_num,
                self.curr_tok.col_num,
                self.original_text,
                list(args),
                self.curr_tok.tok_type,
            )

    def atom(self):
        """
        Parse an atom(pritive) object.
        Grammar:
        atom := | NUM | STR | BOOL | ARRAY | "nil"
        ;; Primitives
        BOOL := "false" | "true"
        ID := LETTER (LETTER | NUM | "-" | "$" | "@")*
        NUM := DIGIT (DIGIT)*
        DIGIT := 1 | 2 | 3| 4 | 5 | 6 | 7 | 8 | 9 | 0
        STR := "\"" (LETTER | NUM )* "\""
        ARRAY := "[" ( or_expr ( "," or_expr )* )? "]"
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
        """
        Parse an arglist rule.
        Grammar:
        arglist := (or_expr ("," or_expr)*)?
        """
        func_args = list()
        while self.curr_tok.tok_type != Tok_Type.RROUND:
            arg_value = self.or_expr()
            func_args.append(arg_value)
            if self.curr_tok.tok_type != Tok_Type.RROUND:
                self.match(Tok_Type.COMMA)
        return func_args

    def access_ident(self):
        # Create ID node
        node = self.match(Tok_Type.ID)
        left = ID_Node(node.lexeme)

        while self.curr_tok.tok_type in [
            Tok_Type.DOT,
            Tok_Type.LSQUARE,
        ]:
            if self.curr_tok.tok_type == Tok_Type.DOT:
                self.match(Tok_Type.DOT)
                property_name = ID_Node(self.match(Tok_Type.ID).lexeme)
                left = Dot_Bin_Node(left, property_name)
            elif self.curr_tok.tok_type == Tok_Type.LSQUARE:
                self.match(Tok_Type.LSQUARE)
                arr_idx = self.atom()
                self.match(Tok_Type.RSQUARE)
                left = Array_Access_Node(left, arr_idx)

        return left

    def access_this(self):
        self.match(Tok_Type.THIS)
        left = ID_Node("this")

        while self.curr_tok.tok_type in [
            Tok_Type.DOT,
            Tok_Type.LSQUARE,
        ]:
            if self.curr_tok.tok_type == Tok_Type.DOT:
                self.match(Tok_Type.DOT)
                property_name = ID_Node(self.match(Tok_Type.ID).lexeme)
                left = Dot_Bin_Node(left, property_name)
            elif self.curr_tok.tok_type == Tok_Type.LSQUARE:
                self.match(Tok_Type.LSQUARE)
                arr_idx = self.atom()
                self.match(Tok_Type.RSQUARE)
                left = Array_Access_Node(left, arr_idx)

        return left

    def access(self):
        if self.curr_tok.tok_type == Tok_Type.ID:
            return self.access_ident()
        elif self.curr_tok.tok_type == Tok_Type.THIS:
            return self.access_this()

    def call_or_access(self):
        """
        Parse a call or access rule.
        Grammar:
        call_or_access := ( ID | "this" ) ( "(" arglist ")" | "." ID )*
        """

        access_node = self.access()
        if self.curr_tok.tok_type == Tok_Type.LROUND:
            self.match(Tok_Type.LROUND)
            func_args = self.arglist()
            self.match(Tok_Type.RROUND)
            return Call_Node(access_node, func_args)
        else:
            return access_node

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
        elif self.curr_tok.tok_type == Tok_Type.LROUND:
            self.match(Tok_Type.LROUND)
            expr = self.or_expr()
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

    def expr_statement(self):
        node = self.or_expr()
        self.match(Tok_Type.SEMIC)
        return node

    def reassign_or_eval_statement(self):
        # There are a couple of cases to handle here:
        # 1. This is a regular expression like "a + 4;"
        # 2. This is a simple variable access like "a.b;" or "a[3];"
        # 3. This is a reassign operation like "a.b = 4;"
        var_name = self.or_expr()
        if isinstance(var_name, (Dot_Bin_Node, ID_Node, This_Node, Array_Access_Node)):
            # TODO: Throw error if we get a "This" node without anything else attached
            # to it.
            if self.curr_tok.tok_type == Tok_Type.ASSIGN:
                self.match(Tok_Type.ASSIGN)
                value = self.expr_statement()
                if isinstance(var_name, (ID_Node, Array_Access_Node)):
                    a = Replace_Assign_Bin_Node(None, var_name, value)
                    return a
                else:
                    a = Replace_Assign_Bin_Node(var_name.left, var_name.right, value)
                    return a
            # TODO: Add augmented assign cases here.
            elif self.curr_tok.tok_type == Tok_Type.ADDASSIGN:
                self.match(Tok_Type.ADDASSIGN)
                value = self.expr_statement()
                if isinstance(var_name, ID_Node):
                    return AddAssign_Node(None, var_name, value)
                else:
                    # Decompose the nodes
                    return AddAssign_Node(var_name.left, var_name.right, value)
            elif self.curr_tok.tok_type == Tok_Type.SUBASSIGN:
                self.match(Tok_Type.SUBASSIGN)
                value = self.expr_statement()
                if isinstance(var_name, ID_Node):
                    return SubAssign_Node(None, var_name, value)
                else:
                    # Decompose the nodes
                    return SubAssign_Node(var_name.left, var_name.right, value)
            else:
                # Case of the node not being an assignment node but a variable access
                self.match(Tok_Type.SEMIC)
                return var_name
        else:
            # Case of a regular expression like "a + 4;"
            self.match(Tok_Type.SEMIC)
            return var_name

    def new_asssign_statement(self):
        self.match(Tok_Type.LET)
        symbol_path = self.call_or_access()
        self.match(Tok_Type.ASSIGN)
        value = self.expr_statement()
        # Check if it is a single node
        if isinstance(symbol_path, ID_Node):
            return New_Assign_Bin_Node(None, symbol_path, value)
        else:
            # Decompose the nodes
            return New_Assign_Bin_Node(symbol_path.left, symbol_path.right, value)

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
        conditions.append({"cond": if_cond, "block": then_block})

        # Parse "elif ... then ..."
        while self.curr_tok.tok_type == Tok_Type.ELIF:
            self.match(Tok_Type.ELIF)
            self.match(Tok_Type.LROUND)
            cond = self.or_expr()
            self.match(Tok_Type.RROUND)
            then_block = self.block()
            conditions.append({"cond": cond, "block": then_block})

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
        """

        self.match(Tok_Type.PRINT)
        expr = self.expr_statement()
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
        """
        Parse a while statement.
        Grammar:
        while_stmnt := "while" "(" or_expr ")" block_stmnt
        """
        self.match(Tok_Type.WHILE)
        self.match(Tok_Type.LROUND)
        condition = self.or_expr()
        self.match(Tok_Type.RROUND)

        body = self.block()
        return While_Node(condition, body)

    def switch_stmnt_case(self):
        """
        Parse a single switch statement case.
        """
        stmnt_block = list()
        while self.curr_tok.tok_type not in [
            Tok_Type.CASE,
            Tok_Type.DEFAULT,
            Tok_Type.RCURLY,
        ]:
            stmnt = self.statement()
            stmnt_block.append(stmnt)

        # We can reuse the block node to evaluate the statements inside of a switch
        # case. The only difference between the two is how parsing is done. Block nodes
        # require curly brackets while switch case statements do not necessarily
        # require them.
        return Scope_Block_Node(stmnt_block)

    def switch_statement(self):
        """
        Parse a switch statement rule.
        Grammar:
        switch_stmnt := "switch" "(" or_expr ")"
                        ("case"  or_expr ":" block_stmnt)*
                        "default" ":" block_stmnt
        """
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

    def class_def(self):
        """
        Parse a class definition rule.
        Grammar:
        class_def := "class" ID "{" func_def* "}"
        """
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
        """
        Parse a flow statement rule.
        Grammar:
        flow_stmnt := ("break" | "continue" | "return" ( or_expr )? ) ";"
        """
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
        """
        Parse a do-while statement.
        Grammar:
        do_while_stmnt := "do" block_stmnt "while" "(" or_expr ")"
        """
        self.match(Tok_Type.DO)
        body = self.block()
        self.match(Tok_Type.WHILE)
        self.match(Tok_Type.LROUND)
        test_cond = self.or_expr()
        self.match(Tok_Type.RROUND)
        self.match(Tok_Type.SEMIC)
        return Do_While_Node(test_cond, body)

    def import_statement(self):
        """
        Parse an import statement.
        Grammar:
        import_stmnt := "import" ID ("as" ID)?
        """
        self.match(Tok_Type.IMPORT)
        module_name = self.match(Tok_Type.ID).lexeme
        import_name = None
        if self.curr_tok.tok_type == Tok_Type.AS:
            self.match(Tok_Type.AS)
            import_name = self.match(Tok_Type.ID).lexeme

        return Import_Node(module_name, import_name)

    def statement(self):
        """
         Parse a single statement.
         Grammar:
        statement := if_stmnt        |
                     while_stmnt     |
                     for_stmnt       |
                     class_def       |
                     func_def        |
                     block_stmnt     |
                     print_stmnt     |
                     switch_stmnt    |
                     flow_stmnt      |
                     do_while_stmnt  |
                     import_stmnt    |
                     simple_expr
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
        elif self.curr_tok.tok_type == Tok_Type.LET:
            return self.new_asssign_statement()
        elif self.curr_tok.tok_type in [Tok_Type.ID, Tok_Type.THIS]:
            return self.reassign_or_eval_statement()
        else:
            return self.expr_statement()

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
