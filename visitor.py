from object_type import ObjectType
from objects import *
from tokens import Tok_Type


class Visitor:
    def __init__(self):
        "Visitor class used to evaluate nodes."
        pass

    def visit(self, node):
        """
        Visit an unspecified node.
        """
        return node.accept(self)

    def visit_program(self, node):
        for stmnt in node.stmnts:
            val = stmnt.accept(self)
            print(val.value)

    def visit_num(self, node):
        return Num_Object(node.val)

    def visit_symbol(self, node):
        # Retrieve symbol from env
        pass

    def visit_string(self, node):
        pass
        # return

    def visit_bracket(self, node):
        return node.expr.accept(self)

    def visit_bool(self, node):
        return Bool_Object(node.val)

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
        result = node.accept(self)
        if node.op == Tok_Type.MINUS:
            pass
        elif node.op == Tok_Type.BANG:
            pass
