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
            print("Program node at head", stmnt)
            val = stmnt.accept(self)
            print(val)

    def visit_num(self, node):
        print("Num visit from node", node)
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
        # Evaluate left and right sides
        # print("Got binary")
        print("visit bin node", node)
        left = node.left.accept(self)
        right = node.right.accept(self)
        print("Left from binary", left)
        print("Right from binary", right)

        # Perform actions depeding on type
        if node.op == Tok_Type.PLUS:
            return left.value + right.value
        elif node.op == Tok_Type.MINUS:
            pass
        elif node.op == Tok_Type.MUL:
            pass
        elif node.op == Tok_Type.DIV:
            pass
        elif node.op == Tok_Type.GT:
            pass
        elif node.op == Tok_Type.GTE:
            pass
        elif node.op == Tok_Type.LT:
            pass
        elif node.op == Tok_Type.LTE:
            pass
        elif node.op == Tok_Type.EQ:
            pass
        elif node.op == Tok_Type.NEQ:
            pass

    def visit_unary(self, node):
        result = node.accept(self)
        if node.op == Tok_Type.MINUS:
            pass
        elif node.op == Tok_Type.BANG:
            pass
