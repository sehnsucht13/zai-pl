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

    def visit_id(self, node):
        # Retrieve id
        pass

    def visit_string(self, node):
        pass

    def visit_bracket(self, node):
        pass

    def visit_bool(self, node):
        return Bool_Object(node.val)

    def visit_binary(self, node):
        print(node)
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
        # >
        elif node.op == Tok_Type.GT:
            result = left.value > right.value
            if result is True:
                return Bool_Object(True)
            else:
                return Bool_Object(False)

        # >=
        elif node.op == Tok_Type.GTE:
            result = left.value >= right.value
            if result is True:
                return Bool_Object(True)
            else:
                return Bool_Object(False)
        # <
        elif node.op == Tok_Type.LT:
            result = left.value < right.value
            if result is True:
                return Bool_Object(True)
            else:
                return Bool_Object(False)
        # <=
        elif node.op == Tok_Type.LTE:
            result = left.value <= right.value
            if result is True:
                return Bool_Object(True)
            else:
                return Bool_Object(False)
        elif node.op == Tok_Type.EQ:
            result = left.value == right.value
            if result is True:
                return Bool_Object(True)
            else:
                return Bool_Object(False)
        elif node.op == Tok_Type.NEQ:
            result = left.value != right.value
            if result is True:
                return Bool_Object(True)
            else:
                return Bool_Object(False)

    def visit_unary(self, node):
        result = node.accept(self)
        if node.op == Tok_Type.MINUS:
            pass
        elif node.op == Tok_Type.BANG:
            pass
