from object_type import ObjectType
from objects import *
from tokens import Tok_Type
from env import Frame


class Visitor:
    def __init__(self):
        "Visitor class used to evaluate nodes."
        self.global_env = Frame()

    def visit(self, node):
        """
        Visit an unspecified node.
        """
        return node.accept(self)

    def visit_program(self, node):
        for stmnt in node.stmnts:
            val = stmnt.accept(self)
            if is_atom(val):
                print(val.value)

    def visit_num(self, node):
        return Num_Object(node.val)

    def visit_symbol(self, node):
        # Retrieve symbol from env
        return self.global_env.lookup_symbol(node.val)

    def visit_string(self, node):
        pass
        # return

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
        if is_atom(print_value):
            print(print_value.value)

    def visit_assign(self, node):
        symbol = node.symbol
        # Evaluate the right hand side
        value = node.value.accept(self)
        # Assign Symbol
        self.global_env.add_symbol(symbol, value)
        # TODO: Should we return its value after assignment?

    def visit_block(self, node):
        # Create a new scope to evaluate the current block in
        self.global_env.enter_scope()
        for stmnt in node.stmnts:
            stmnt.accept(self)
        self.global_env.exit_scope()
