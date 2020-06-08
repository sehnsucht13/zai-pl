from object_type import ObjectType
from objects import *
from tokens import Tok_Type
from env import RunTime_Stack


class Visitor:
    """ Visitor class used to evaluate AST nodes. """

    def __init__(self):
        "Visitor class used to evaluate nodes."
        self.global_env = RunTime_Stack()

    def visit(self, ast_root):
        """
        Main entry point for all AST roots.
        """
        return ast_root.accept(self)

    def visit_program(self, node):
        for stmnt in node.stmnts:
            val = stmnt.accept(self)
            if is_atom(val):
                pprint_internal_object(val)

    def visit_num(self, node):
        return Num_Object(node.val)

    def visit_symbol(self, node):
        # Retrieve symbol from env
        # return self.global_env.lookup_symbol(node.val)
        curr_frame = self.global_env.peek()
        # TODO: Catch case of symbol not existing. Need to return an error
        return curr_frame.resolve_sym(node.val)

    def visit_string(self, node):
        pass

    def visit_bracket(self, node):
        return node.expr.accept(self)

    def visit_bool(self, node):
        if node.val == Tok_Type.TRUE:
            return Bool_Object(True)
        else:
            return Bool_Object(False)

    def visit_arith(self, node):
        # Evaluate left and right sides
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Perform actions depeding on type
        if node.op == Tok_Type.PLUS:
            return Num_Object(left.value + right.value)
        elif node.op == Tok_Type.MINUS:
            return Num_Object(left.value - right.value)
        elif node.op == Tok_Type.MUL:
            return Num_Object(left.value * right.value)
        elif node.op == Tok_Type.DIV:
            return Num_Object(left.value / right.value)

    def visit_relop(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Stores the result of the operation
        relop_result = None

        # >
        if node.op == Tok_Type.GT:
            relop_result = left.value > right.value
        # >=
        elif node.op == Tok_Type.GTE:
            relop_result = left.value >= right.value
        # <
        elif node.op == Tok_Type.LT:
            relop_result = left.value < right.value
        # <=
        elif node.op == Tok_Type.LTE:
            relop_result = left.value <= right.value

        return Bool_Object(relop_result)

    def visit_eq(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        # Store the result of the comparison
        eq_result = None
        if node.op == Tok_Type.EQ:
            eq_result = left.value == right.value
        elif node.op == Tok_Type.NEQ:
            eq_result = left.value != right.value

        return Bool_Object(eq_result)

    def visit_unary(self, node):
        result = node.value.accept(self)
        if node.op == Tok_Type.MINUS:
            return Num_Object(-(result.value))
        elif node.op == Tok_Type.BANG:
            return Bool_Object(not (result.value))

    def visit_if(self, node):
        condition = node.condition.accept(self)
        if condition.value is True:
            return node.true_stmnt.accept(self)
        else:
            return node.else_stmnt.accept(self)

    def visit_print(self, node):
        print_value = node.expr.accept(self)
        pprint_internal_object(print_value)

    def visit_assign(self, node):
        symbol = node.symbol
        # Evaluate the right hand side
        value = node.value.accept(self)
        curr_frame = self.global_env.peek()
        curr_frame.add_symbol(symbol, value)
        # TODO: Should we return its value after assignment?

    def visit_block(self, node):
        # Create a new scope to evaluate the current block in
        curr_frame = self.global_env.peek()
        curr_frame.enter_scope()
        for stmnt in node.stmnts:
            stmnt.accept(self)
        curr_frame.exit_scope()

    def visit_func_def(self, node):
        curr_frame = self.global_env.peek()
        # Register the function in the current frame
        curr_frame.add_symbol(
            node.name, Func_Object(node.name, node.args, node.body, curr_frame)
        )
