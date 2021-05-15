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
    ThisNode,
    StringNode,
    NumNode,
    ArrayNode,
    ArrayAccessNode,
    NilNode,
    BoolNode,
    ArithBinNode,
    SymbolNode,
    DotBinNode,
    BracketNode,
    UnaryNode,
    IncrNode,
    DecrNode,
    CallNode,
    AddassignNode,
    SubassignNode,
    NewAssignBinNode,
    IfNode,
    PrintNode,
    FuncNode,
    ScopeBlockNode,
    WhileNode,
    BreakNode,
    ContinueNode,
    DoWhileNode,
    ImportNode,
    ProgramNode,
    SwitchNode,
    ClassDefNode,
    ClassMethodNode,
    ReturnNode,
    ReplaceAssignBinNode,
    RelopBinNode,
    EqBinNode,
    LogicBinNode,
)
from zai.tokens import TokType
from zai.internal_error import InternalParseError


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
            raise InternalParseError(
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
        if self.curr_tok.tok_type == TokType.THIS:
            self.match(TokType.THIS)
            return ThisNode()
        elif self.curr_tok.tok_type == TokType.DQUOTE:
            self.match(TokType.DQUOTE)
            str_token = self.match(TokType.STRING)
            node = StringNode(str_token.lexeme)
            self.match(TokType.DQUOTE)
            return node
        elif self.curr_tok.tok_type == TokType.NUM:
            node = self.match(TokType.NUM)
            return NumNode(node.lexeme)
        elif self.curr_tok.tok_type == TokType.LSQUARE:
            self.match(TokType.LSQUARE)
            array_elem = list()
            while self.curr_tok.tok_type != TokType.RSQUARE:
                arg_value = self.or_expr()
                array_elem.append(arg_value)
                if self.curr_tok.tok_type != TokType.RSQUARE:
                    self.match(TokType.COMMA)
            self.match(TokType.RSQUARE)
            return ArrayNode(array_elem)
        elif self.curr_tok.tok_type == TokType.NIL:
            self.match(TokType.NIL)
            return NilNode()
        else:
            node = self.match(TokType.TRUE, TokType.FALSE)
            return BoolNode(node.tok_type)

    def arglist(self):
        """
        Parse an arglist rule.
        Grammar:
        arglist := (or_expr ("," or_expr)*)?
        """
        func_args = list()
        while self.curr_tok.tok_type != TokType.RROUND:
            arg_value = self.or_expr()
            func_args.append(arg_value)
            if self.curr_tok.tok_type != TokType.RROUND:
                self.match(TokType.COMMA)
        return func_args

    def access_ident(self):
        # Create ID node
        node = self.match(TokType.ID)
        left = SymbolNode(node.lexeme)

        while self.curr_tok.tok_type in [
            TokType.DOT,
            TokType.LSQUARE,
        ]:
            if self.curr_tok.tok_type == TokType.DOT:
                self.match(TokType.DOT)
                property_name = SymbolNode(self.match(TokType.ID).lexeme)
                left = DotBinNode(left, property_name)
            elif self.curr_tok.tok_type == TokType.LSQUARE:
                self.match(TokType.LSQUARE)
                arr_idx = self.atom()
                self.match(TokType.RSQUARE)
                left = ArrayAccessNode(left, arr_idx)

        return left

    def access_this(self):
        self.match(TokType.THIS)
        left = SymbolNode("this")

        while self.curr_tok.tok_type in [
            TokType.DOT,
            TokType.LSQUARE,
        ]:
            if self.curr_tok.tok_type == TokType.DOT:
                self.match(TokType.DOT)
                property_name = SymbolNode(self.match(TokType.ID).lexeme)
                left = DotBinNode(left, property_name)
            elif self.curr_tok.tok_type == TokType.LSQUARE:
                self.match(TokType.LSQUARE)
                arr_idx = self.atom()
                self.match(TokType.RSQUARE)
                left = ArrayAccessNode(left, arr_idx)

        return left

    def access(self):
        if self.curr_tok.tok_type == TokType.ID:
            return self.access_ident()
        elif self.curr_tok.tok_type == TokType.THIS:
            return self.access_this()

    def call_or_access(self):
        """
        Parse a call or access rule.
        Grammar:
        call_or_access := ( ID | "this" ) ( "(" arglist ")" | "." ID )*
        """

        access_node = self.access()
        if self.curr_tok.tok_type == TokType.LROUND:
            self.match(TokType.LROUND)
            func_args = self.arglist()
            self.match(TokType.RROUND)
            return CallNode(access_node, func_args)
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
            TokType.ID,
            TokType.THIS,
        ]:
            return self.call_or_access()
        elif self.curr_tok.tok_type == TokType.LROUND:
            self.match(TokType.LROUND)
            expr = self.or_expr()
            self.match(TokType.RROUND)
            return BracketNode(expr)
        elif self.curr_tok.tok_type in [TokType.BANG, TokType.MINUS]:
            op = self.match(TokType.BANG, TokType.MINUS)
            fact = self.factor()
            return UnaryNode(op.tok_type, fact)
        # TODO: Handle case of it being an "ID" token instead of just num.
        elif self.curr_tok.tok_type in [TokType.NUM, TokType.ID] and self.peek() in [
            TokType.INCR,
            TokType.DECR,
        ]:
            # Evaluate the initial number token
            node = self.atom()

            # "++" or "--" operators can be nested
            while self.curr_tok.tok_type in [TokType.INCR, TokType.DECR]:
                op = self.match(TokType.INCR, TokType.DECR)
                if op.tok_type == TokType.INCR:
                    node = IncrNode(node)
                elif op.tok_type == TokType.DECR:
                    node = DecrNode(node)
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
        while self.curr_tok.tok_type in [TokType.MUL, TokType.DIV]:
            op = self.match(TokType.MUL, TokType.DIV)
            right = self.factor()
            left = ArithBinNode(left, op.tok_type, right)

        return left

    def add_expr(self):
        """
        Parse an addition expression:
        Grammar:
        add_expr := term (("+" | "-") term)*
        """
        left = self.term()
        while self.curr_tok.tok_type in [TokType.PLUS, TokType.MINUS]:
            op = self.match(TokType.PLUS, TokType.MINUS)
            right = self.term()
            left = ArithBinNode(left, op.tok_type, right)

        return left

    def rel_expr(self):
        """
        Parse a relative expression:
        Grammar:
        rel_expr := add_expr ( ("<" | ">" | "<=" | ">=") add_expr)*
        """

        left = self.add_expr()
        while self.curr_tok.tok_type in [
            TokType.GT,
            TokType.GTE,
            TokType.LT,
            TokType.LTE,
        ]:
            op = self.match(TokType.GT, TokType.GTE, TokType.LT, TokType.LTE)
            right = self.add_expr()
            left = RelopBinNode(left, op.tok_type, right)

        return left

    def eq_expr(self):
        """
        Parse an equality expression:
        Grammar:
        eq_expr := rel_expr ( ("=="|"!=") rel_expr)*
        """
        left = self.rel_expr()
        while self.curr_tok.tok_type in [TokType.EQ, TokType.NEQ]:
            op = self.match(TokType.EQ, TokType.NEQ)
            right = self.rel_expr()
            left = EqBinNode(left, op.tok_type, right)

        return left

    def and_expr(self):
        """
        Parse an equality expression:
        Grammar:
        and_expr := eq_expr ("&&" eq_expr)*
        """
        left = self.eq_expr()
        while self.curr_tok.tok_type == TokType.AND:
            op = self.match(TokType.AND)
            right = self.eq_expr()
            left = LogicBinNode(left, op.tok_type, right)

        return left

    def or_expr(self):
        """
        Parse an equality expression:
        Grammar:
        or_expr := and_expr ("||" and_expr)*
        """
        left = self.and_expr()
        while self.curr_tok.tok_type == TokType.OR:
            op = self.match(TokType.OR)
            right = self.and_expr()
            left = LogicBinNode(left, op.tok_type, right)

        return left

    def expr_statement(self):
        node = self.or_expr()
        self.match(TokType.SEMIC)
        return node

    def reassign_or_eval_statement(self):
        # There are a couple of cases to handle here:
        # 1. This is a regular expression like "a + 4;"
        # 2. This is a simple variable access like "a.b;" or "a[3];"
        # 3. This is a reassign operation like "a.b = 4;"
        var_name = self.or_expr()
        if isinstance(var_name, (DotBinNode, SymbolNode, ThisNode, ArrayAccessNode)):
            # TODO: Throw error if we get a "This" node without anything else attached
            # to it.
            if self.curr_tok.tok_type == TokType.ASSIGN:
                self.match(TokType.ASSIGN)
                value = self.expr_statement()
                if isinstance(var_name, (SymbolNode, ArrayAccessNode)):
                    a = ReplaceAssignBinNode(None, var_name, value)
                    return a
                else:
                    a = ReplaceAssignBinNode(var_name.left, var_name.right, value)
                    return a
            # TODO: Add augmented assign cases here.
            elif self.curr_tok.tok_type == TokType.ADDASSIGN:
                self.match(TokType.ADDASSIGN)
                value = self.expr_statement()
                if isinstance(var_name, SymbolNode):
                    return AddassignNode(None, var_name, value)
                else:
                    # Decompose the nodes
                    return AddassignNode(var_name.left, var_name.right, value)
            elif self.curr_tok.tok_type == TokType.SUBASSIGN:
                self.match(TokType.SUBASSIGN)
                value = self.expr_statement()
                if isinstance(var_name, SymbolNode):
                    return SubassignNode(None, var_name, value)
                else:
                    # Decompose the nodes
                    return SubassignNode(var_name.left, var_name.right, value)
            else:
                # Case of the node not being an assignment node but a variable access
                self.match(TokType.SEMIC)
                return var_name
        else:
            # Case of a regular expression like "a + 4;"
            self.match(TokType.SEMIC)
            return var_name

    def new_asssign_statement(self):
        self.match(TokType.LET)
        symbol_path = self.call_or_access()
        self.match(TokType.ASSIGN)
        value = self.expr_statement()
        # Check if it is a single node
        if symbol_path is None:
            raise InternalParseError(
                self.curr_tok.line_num,
                self.curr_tok.col_num,
                self.original_text,
                TokType.ID,
                self.curr_tok.tok_type,
            )
        elif isinstance(symbol_path, SymbolNode):
            return NewAssignBinNode(None, symbol_path, value)
        else:
            # Decompose the nodes
            return NewAssignBinNode(symbol_path.left, symbol_path.right, value)

    def if_statement(self):
        """
        Parse an if statement.
        Grammar:

        if_stmnt := "if" "(" expression ")" statement ( "else" statement )?
        """
        # List used to store all "if condition then" or "elif condition then" pairs.
        conditions = list()

        # Parse "If ... then ..."
        self.match(TokType.IF)
        self.match(TokType.LROUND)
        if_cond = self.or_expr()
        self.match(TokType.RROUND)
        then_block = self.block()
        conditions.append({"cond": if_cond, "block": then_block})

        # Parse "elif ... then ..."
        while self.curr_tok.tok_type == TokType.ELIF:
            self.match(TokType.ELIF)
            self.match(TokType.LROUND)
            cond = self.or_expr()
            self.match(TokType.RROUND)
            then_block = self.block()
            conditions.append({"cond": cond, "block": then_block})

        else_block = None
        if self.curr_tok.tok_type == TokType.ELSE:
            self.match(TokType.ELSE)
            else_block = self.block()

        node = IfNode(conditions, else_block)
        return node

    def print_statement(self):
        """
        Parse a print statement.
        Grammar:
        """

        self.match(TokType.PRINT)
        expr = self.expr_statement()
        return PrintNode(expr)

    # TODO: Refactor match function and finish parsing functions
    def func_def(self):
        """
        Parse a function definition.
        Grammar:

        func_def := "func" ID "(" ID? ("," ID)* ")" "{" statement* "}"
        """

        self.match(TokType.FUNC)
        func_name = self.match(TokType.ID).lexeme
        self.match(TokType.LROUND)

        # Collect argument symbols for the function
        arg_symbols = list()
        if self.curr_tok.tok_type == TokType.ID:
            func_arg = self.match(TokType.ID)
            arg_symbols.append(func_arg)
            if self.curr_tok.tok_type == TokType.COMMA:
                while self.curr_tok.tok_type != TokType.RROUND:
                    self.match(TokType.COMMA)
                    func_arg = self.match(TokType.ID)
                    arg_symbols.append(func_arg)

        self.match(TokType.RROUND)
        self.match(TokType.LCURLY)

        func_body = list()
        while self.curr_tok.tok_type != TokType.RCURLY:
            func_stmnt = self.statement()
            func_body.append(func_stmnt)
        self.match(TokType.RCURLY)

        return FuncNode(func_name, arg_symbols, func_body)

    def block(self):
        """
        Parse a block which acts as a nested scope within the program.
        Grammar:

        block := "{" statement* "}"
        """

        self.match(TokType.LCURLY)
        block_stmnts = list()
        while self.curr_tok.tok_type != TokType.RCURLY:
            stmnt = self.statement()
            block_stmnts.append(stmnt)
        self.match(TokType.RCURLY)
        return ScopeBlockNode(block_stmnts)

    def while_statement(self):
        """
        Parse a while statement.
        Grammar:
        while_stmnt := "while" "(" or_expr ")" block_stmnt
        """
        self.match(TokType.WHILE)
        self.match(TokType.LROUND)
        condition = self.or_expr()
        self.match(TokType.RROUND)

        body = self.block()
        return WhileNode(condition, body)

    def switch_stmnt_case(self):
        """
        Parse a single switch statement case.
        """
        stmnt_block = list()
        while self.curr_tok.tok_type not in [
            TokType.CASE,
            TokType.DEFAULT,
            TokType.RCURLY,
        ]:
            stmnt = self.statement()
            stmnt_block.append(stmnt)

        # We can reuse the block node to evaluate the statements inside of a switch
        # case. The only difference between the two is how parsing is done. Block nodes
        # require curly brackets while switch case statements do not necessarily
        # require them.
        return ScopeBlockNode(stmnt_block)

    def switch_statement(self):
        """
        Parse a switch statement rule.
        Grammar:
        switch_stmnt := "switch" "(" or_expr ")"
                        ("case"  or_expr ":" block_stmnt)*
                        "default" ":" block_stmnt
        """
        self.match(TokType.SWITCH)
        self.match(TokType.LROUND)
        switch_cond = self.or_expr()
        self.match(TokType.RROUND)
        self.match(TokType.LCURLY)

        cases = list()
        while self.curr_tok.tok_type == TokType.CASE:
            self.match(TokType.CASE)
            test_cond = self.or_expr()
            self.match(TokType.COLON)
            block = self.switch_stmnt_case()
            cases.append(tuple((test_cond, block)))

        self.match(TokType.DEFAULT)
        self.match(TokType.COLON)
        default_block = self.switch_stmnt_case()
        self.match(TokType.RCURLY)

        return SwitchNode(switch_cond, cases, default_block)

    def class_def(self):
        """
        Parse a class definition rule.
        Grammar:
        class_def := "class" ID "{" func_def* "}"
        """
        self.match(TokType.CLASS)
        class_name = self.match(TokType.ID).lexeme
        self.match(TokType.LCURLY)

        class_methods = list()
        while self.curr_tok.tok_type != TokType.RCURLY:
            func_node = self.func_def()
            # Cast regular function node to method node.
            # The parsing procedure is the same for both so there is no point
            # in rewriting the code in a separate parsing procedure.
            method_node = ClassMethodNode(func_node.name, func_node.args, func_node.body)
            class_methods.append(method_node)

        self.match(TokType.RCURLY)

        return ClassDefNode(class_name, class_methods)

    def flow_statement(self):
        """
        Parse a flow statement rule.
        Grammar:
        flow_stmnt := ("break" | "continue" | "return" ( or_expr )? ) ";"
        """
        node = None
        if self.curr_tok.tok_type == TokType.RETURN:
            return_val = None
            self.match(TokType.RETURN)
            # Check if the return statement contains an expression or not.
            if self.curr_tok.tok_type != TokType.SEMIC:
                return_val = self.or_expr()

            node = ReturnNode(return_val)
        elif self.curr_tok.tok_type == TokType.BREAK:
            self.match(TokType.BREAK)
            node = BreakNode()
        elif self.curr_tok.tok_type == TokType.CONTINUE:
            self.match(TokType.CONTINUE)
            node = ContinueNode()

        self.match(TokType.SEMIC)
        return node

    def do_while_statement(self):
        """
        Parse a do-while statement.
        Grammar:
        do_while_stmnt := "do" block_stmnt "while" "(" or_expr ")"
        """
        self.match(TokType.DO)
        body = self.block()
        self.match(TokType.WHILE)
        self.match(TokType.LROUND)
        test_cond = self.or_expr()
        self.match(TokType.RROUND)
        self.match(TokType.SEMIC)
        return DoWhileNode(test_cond, body)

    def import_statement(self):
        """
        Parse an import statement.
        Grammar:
        import_stmnt := "import" ID ("as" ID)?
        """
        self.match(TokType.IMPORT)
        module_name = self.match(TokType.ID).lexeme
        import_name = None
        if self.curr_tok.tok_type == TokType.AS:
            self.match(TokType.AS)
            import_name = self.match(TokType.ID).lexeme

        return ImportNode(module_name, import_name)

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
        if self.curr_tok.tok_type == TokType.IF:
            return self.if_statement()
        elif self.curr_tok.tok_type == TokType.FUNC:
            return self.func_def()
        elif self.curr_tok.tok_type == TokType.CLASS:
            return self.class_def()
        elif self.curr_tok.tok_type == TokType.WHILE:
            return self.while_statement()
        elif self.curr_tok.tok_type == TokType.SWITCH:
            return self.switch_statement()
        elif self.curr_tok.tok_type == TokType.LCURLY:
            return self.block()
        elif self.curr_tok.tok_type == TokType.PRINT:
            return self.print_statement()
        elif self.curr_tok.tok_type == TokType.SWITCH:
            return self.switch_statement()
        elif self.curr_tok.tok_type == TokType.DO:
            return self.do_while_statement()
        elif self.curr_tok.tok_type == TokType.IMPORT:
            return self.import_statement()
        elif self.curr_tok.tok_type in [
            TokType.RETURN,
            TokType.CONTINUE,
            TokType.BREAK,
        ]:
            return self.flow_statement()
        elif self.curr_tok.tok_type == TokType.LET:
            return self.new_asssign_statement()
        elif self.curr_tok.tok_type in [TokType.ID, TokType.THIS]:
            return self.reassign_or_eval_statement()
        else:
            return self.expr_statement()

    def program(self):
        """
        Parse a program rule.
        Grammar:
        program := statement*
        """
        prog_node = ProgramNode()
        while self.curr_tok.tok_type != TokType.EOF:
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
