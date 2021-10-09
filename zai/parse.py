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

import zai.ast_nodes as ast_nodes
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
        """
        # if self.curr_tok.tok_type == TokType.THIS:
        #     self.match(TokType.THIS)
        #     return ThisNode()
        if self.curr_tok.tok_type == TokType.DQUOTE:
            self.match(TokType.DQUOTE)
            str_token = self.match(TokType.STRING)
            node = ast_nodes.StringNode(str_token.lexeme)
            self.match(TokType.DQUOTE)
            return node
        elif self.curr_tok.tok_type == TokType.INT:
            node = self.match(TokType.INT)
            return ast_nodes.IntNode(node.lexeme)
        elif self.curr_tok.tok_type == TokType.FLOAT:
            node = self.match(TokType.FLOAT)
            return ast_nodes.FloatNode(node.lexeme)
        elif self.curr_tok.tok_type == TokType.LSQUARE:
            self.match(TokType.LSQUARE)
            array_elem = list()
            while self.curr_tok.tok_type != TokType.RSQUARE:
                arg_value = self.or_expr()
                array_elem.append(arg_value)
                if self.curr_tok.tok_type != TokType.RSQUARE:
                    self.match(TokType.COMMA)
            self.match(TokType.RSQUARE)
            return ast_nodes.ArrayNode(array_elem)
        elif self.curr_tok.tok_type == TokType.NIL:
            self.match(TokType.NIL)
            return ast_nodes.NilNode()
        else:
            node = self.match(TokType.TRUE, TokType.FALSE)
            return ast_nodes.BoolNode(node.tok_type)

    def arglist(self):
        """
        Parse an arglist rule.
        """
        func_args = list()
        while self.curr_tok.tok_type != TokType.RROUND:
            arg_value = self.or_expr()
            func_args.append(arg_value)
            if self.curr_tok.tok_type != TokType.RROUND:
                self.match(TokType.COMMA)
        return func_args

    def access(self):
        left = None

        if self.curr_tok.tok_type == TokType.ID:
            node = self.match(TokType.ID)
            left = ast_nodes.SymbolNode(node.lexeme)

        while self.curr_tok in [TokType.LSQUARE, TokType.LROUND, TokType.DOT]:
            if self.curr_tok.tok_type == TokType.DOT:
                self.match(TokType.DOT)
                node = self.match(TokType.ID)
                property_name = ast_nodes.SymbolNode(node.lexeme)
                left = ast_nodes.PropertyAccessNode(left, property_name)
                print("Here", left)
            elif self.curr_tok.tok_type == TokType.LSQUARE:
                self.match(TokType.LSQUARE)
                arr_idx = self.or_expr()
                self.match(TokType.RSQUARE)
                left = ast_nodes.ArrayAccessNode(left, arr_idx)
            elif self.curr_tok.tok_type == TokType.LROUND:
                self.match(TokType.LROUND)
                func_args = self.arglist()
                self.match(TokType.RROUND)
                left = ast_nodes.CallNode(left, func_args)

        return left

    def factor(self):
        """
        Parse a factor rule.
        """
        assert self.curr_tok is not None
        if self.curr_tok.tok_type in [
            TokType.ID,
            TokType.THIS,
        ]:
            return self.access()
        elif self.curr_tok.tok_type == TokType.LROUND:
            self.match(TokType.LROUND)
            expr = self.or_expr()
            self.match(TokType.RROUND)
            return ast_nodes.BracketNode(expr)
        elif self.curr_tok.tok_type in [TokType.BANG, TokType.MINUS]:
            op = self.match(TokType.BANG, TokType.MINUS)
            fact = self.factor()
            return ast_nodes.UnaryNode(op.tok_type, fact)
        # TODO: Handle case of it being an "ID" token instead of just num.
        elif self.curr_tok.tok_type in [TokType.INT, TokType.ID] and self.peek() in [
            TokType.INCR,
            TokType.DECR,
        ]:
            # Evaluate the initial number token
            node = self.atom()

            # "++" or "--" operators can be nested
            while self.curr_tok.tok_type in [TokType.INCR, TokType.DECR]:
                op = self.match(TokType.INCR, TokType.DECR)
                if op.tok_type == TokType.INCR:
                    node = ast_nodes.IncrNode(node)
                elif op.tok_type == TokType.DECR:
                    node = ast_nodes.DecrNode(node)
            return node
        else:
            return self.atom()

    def term(self):
        """
        Parse a term rule.
        """
        left = self.factor()
        while self.curr_tok.tok_type in [TokType.MUL, TokType.DIV]:
            op = self.match(TokType.MUL, TokType.DIV)
            right = self.factor()
            left = ast_nodes.ArithBinNode(left, op.tok_type, right)

        return left

    def add_expr(self):
        """
        Parse an addition expression.
        """
        left = self.term()
        while self.curr_tok.tok_type in [TokType.PLUS, TokType.MINUS]:
            op = self.match(TokType.PLUS, TokType.MINUS)
            right = self.term()
            left = ast_nodes.ArithBinNode(left, op.tok_type, right)

        return left

    def rel_expr(self):
        """
        Parse a relative expression:
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
            left = ast_nodes.RelopBinNode(left, op.tok_type, right)

        return left

    def eq_expr(self):
        """
        Parse an equality expression:
        """
        left = self.rel_expr()
        while self.curr_tok.tok_type in [TokType.EQ, TokType.NEQ]:
            op = self.match(TokType.EQ, TokType.NEQ)
            right = self.rel_expr()
            left = ast_nodes.EqBinNode(left, op.tok_type, right)

        return left

    def and_expr(self):
        """
        Parse an equality expression:
        """
        left = self.eq_expr()
        while self.curr_tok.tok_type == TokType.AND:
            op = self.match(TokType.AND)
            right = self.eq_expr()
            left = ast_nodes.LogicBinNode(left, op.tok_type, right)

        return left

    def or_expr(self):
        """
        Parse an equality expression:
        """
        left = self.and_expr()
        while self.curr_tok.tok_type == TokType.OR:
            op = self.match(TokType.OR)
            right = self.and_expr()
            left = ast_nodes.LogicBinNode(left, op.tok_type, right)

        return left

    def assign_expr(self):
        left = self.or_expr()

        if self.curr_tok.tok_type == TokType.ASSIGN:
            if isinstance(left, (ast_nodes.PropertyAccessNode)):
                self.match(TokType.ASSIGN)
                value = self.or_expr()

                return ast_nodes.ReassignBinNode(symbol_path=left.left, symbol_name=left.right, value=value)

            elif isinstance(left, (ast_nodes.SymbolNode, ast_nodes.ArrayAccessNode)):
                self.match(TokType.ASSIGN)
                value = self.or_expr()

                return ast_nodes.ReassignBinNode(symbol_path=None, symbol_name=left, value=value)
            else:
                print("Error! Cannot assign value to non symbol")
        else:
            return left

    def expr_statement(self):
        node = self.assign_expr()
        self.match(TokType.SEMIC)

        return node

    # def _reassign_or_eval_statement(self):
    #     # There are a couple of cases to handle here:
    #     # 1. This is a regular expression like "a + 4;"
    #     # 2. This is a simple variable access like "a.b;" or "a[3];"
    #     # 3. This is a reassign operation like "a.b = 4;"
    #     var_name = self.or_expr()
    #     if isinstance(var_name, (ast_nodes.PropertyAccessNode, ast_nodes.SymbolNode, ThisNode,
    # ast_nodes.ArrayAccessNode)):
    #         # TODO: Throw error if we get a "This" node without anything else attached
    #         # to it.
    #         if self.curr_tok.tok_type == TokType.ASSIGN:
    #             self.match(TokType.ASSIGN)
    #             value = self.expr_statement()
    #             if isinstance(var_name, (ast_nodes.SymbolNode, ast_nodes.ArrayAccessNode)):
    #                 a = ast_nodes.ReassignBinNode(None, var_name, value)
    #                 return a
    #             else:
    #                 a = ast_nodes.ReassignBinNode(var_name.left, var_name.right, value)
    #                 return a
    #         # TODO: Add augmented assign cases here.
    #         elif self.curr_tok.tok_type == TokType.ADDASSIGN:
    #             self.match(TokType.ADDASSIGN)
    #             value = self.expr_statement()
    #             if isinstance(var_name, ast_nodes.SymbolNode):
    #                 return AddassignNode(None, var_name, value)
    #             else:
    #                 # Decompose the nodes
    #                 return AddassignNode(var_name.left, var_name.right, value)
    #         elif self.curr_tok.tok_type == TokType.SUBASSIGN:
    #             self.match(TokType.SUBASSIGN)
    #             value = self.expr_statement()
    #             if isinstance(var_name, ast_nodes.SymbolNode):
    #                 return SubassignNode(None, var_name, value)
    #             else:
    #                 # Decompose the nodes
    #                 return SubassignNode(var_name.left, var_name.right, value)
    #         else:
    #             # Case of the node not being an assignment node but a variable access
    #             self.match(TokType.SEMIC)
    #             return var_name
    #     else:
    #         # Case of a regular expression like "a + 4;"
    #         self.match(TokType.SEMIC)
    #         return var_name

    def new_asssign_statement(self):
        self.match(TokType.LET)
        left = self.access()
        self.match(TokType.ASSIGN)
        value = self.or_expr()
        self.match(TokType.SEMIC)

        if isinstance(left, ast_nodes.PropertyAccessNode):
            return ast_nodes.NewAssignBinNode(symbol_path=left.left, symbol_name=left.right, value=value)
        else:
            return ast_nodes.NewAssignBinNode(symbol_path=None, symbol_name=left, value=value)

    def if_statement(self):
        """
        Parse an if statement.
        """
        from collections import namedtuple

        IfStatementMember = namedtuple("IfStatementMember", ["test_condition", "body"])

        # List used to store all "if condition then" or "elif condition then" pairs.
        conditions = list()

        self.match(TokType.IF)
        self.match(TokType.LROUND)
        condition = self.or_expr()
        self.match(TokType.RROUND)
        body = self.block()
        conditions.append(IfStatementMember(condition, body))

        while self.curr_tok.tok_type == TokType.ELIF:
            self.match(TokType.ELIF)
            self.match(TokType.LROUND)
            condition = self.or_expr()
            self.match(TokType.RROUND)
            body = self.block()
            conditions.append(IfStatementMember(condition, body))

        else_block = None
        if self.curr_tok.tok_type == TokType.ELSE:
            self.match(TokType.ELSE)
            else_block = self.block()

        node = ast_nodes.IfNode(conditions, else_block)
        return node

    def print_statement(self):
        """
        Parse a print statement.
        """

        self.match(TokType.PRINT)
        expr = self.expr_statement()
        return ast_nodes.PrintNode(expr)

    # TODO: Refactor match function and finish parsing functions
    def func_def(self):
        """
        Parse a function definition.
        """

        self.match(TokType.FUNC)
        func_name = self.match(TokType.ID).lexeme
        self.match(TokType.LROUND)

        # Collect argument symbols for the function
        func_args = list()
        if self.curr_tok.tok_type == TokType.ID:
            arg = self.match(TokType.ID)
            func_args.append(arg)
            if self.curr_tok.tok_type == TokType.COMMA:
                while self.curr_tok.tok_type != TokType.RROUND:
                    self.match(TokType.COMMA)
                    arg = self.match(TokType.ID)
                    func_args.append(arg)

        self.match(TokType.RROUND)
        self.match(TokType.LCURLY)

        func_body = list()
        while self.curr_tok.tok_type != TokType.RCURLY:
            func_stmnt = self.statement()
            func_body.append(func_stmnt)
        self.match(TokType.RCURLY)

        return ast_nodes.FuncNode(func_name, func_args, func_body)

    def block(self):
        """
        Parse a block which acts as a nested scope within the program.
        """

        self.match(TokType.LCURLY)
        block_stmnts = list()
        while self.curr_tok.tok_type != TokType.RCURLY:
            stmnt = self.statement()
            block_stmnts.append(stmnt)
        self.match(TokType.RCURLY)
        return ast_nodes.BlockNode(block_stmnts)

    def while_statement(self):
        """
        Parse a while statement.
        """
        self.match(TokType.WHILE)
        self.match(TokType.LROUND)
        condition = self.or_expr()
        self.match(TokType.RROUND)

        body = self.block()
        return ast_nodes.WhileNode(condition, body)

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
        return ast_nodes.BlockNode(stmnt_block)

    def switch_statement(self):
        """
        Parse a switch statement rule.
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

        return ast_nodes.SwitchNode(switch_cond, cases, default_block)

    def class_def(self):
        """
        Parse a class definition rule.
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
            method_node = ast_nodes.ClassMethodNode(func_node.name, func_node.args, func_node.body)
            class_methods.append(method_node)

        self.match(TokType.RCURLY)

        return ast_nodes.ClassDefNode(class_name, class_methods)

    def flow_statement(self):
        """
        Parse a flow statement rule.
        """
        node = None
        if self.curr_tok.tok_type == TokType.RETURN:
            return_val = None
            self.match(TokType.RETURN)
            # Check if the return statement contains an expression or not.
            if self.curr_tok.tok_type != TokType.SEMIC:
                return_val = self.or_expr()

            node = ast_nodes.ReturnNode(return_val)
        elif self.curr_tok.tok_type == TokType.BREAK:
            self.match(TokType.BREAK)
            node = ast_nodes.BreakNode()
        elif self.curr_tok.tok_type == TokType.CONTINUE:
            self.match(TokType.CONTINUE)
            node = ast_nodes.ContinueNode()

        self.match(TokType.SEMIC)
        return node

    def do_while_statement(self):
        """
        Parse a do-while statement.
        """
        self.match(TokType.DO)
        body = self.block()
        self.match(TokType.WHILE)
        self.match(TokType.LROUND)
        test_cond = self.or_expr()
        self.match(TokType.RROUND)
        self.match(TokType.SEMIC)
        return ast_nodes.DoWhileNode(test_cond, body)

    def import_statement(self):
        """
        Parse an import statement.
        """
        self.match(TokType.IMPORT)
        module_name = self.match(TokType.ID).lexeme
        import_name = None
        if self.curr_tok.tok_type == TokType.AS:
            self.match(TokType.AS)
            import_name = self.match(TokType.ID).lexeme

        return ast_nodes.ImportNode(module_name, import_name)

    def statement(self):
        """
        Parse a single statement.
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
        # elif self.curr_tok.tok_type in [TokType.ID, TokType.THIS]:
        #     return self.reassign_or_eval_statement()
        else:
            # self.assign_expr()
            return self.expr_statement()

    def program(self):
        """
        Parse a program rule.
        """
        prog_node = ast_nodes.ProgramNode()
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
