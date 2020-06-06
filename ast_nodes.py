class AST_Node:
    def __init__(self):
        raise NotImplementedError()


class Program_Node(AST_Node):
    def __init__(self):
        self.stmnts = list()

    def add_stmnt(self, stmnt):
        self.stmnts.append(stmnt)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_program(self)

    def __str__(self):
        stmnt_string = str()
        for stmnt in self.stmnts:
            stmnt_string += "\n" + stmnt.__str__()


class Bin_Node(AST_Node):
    def __init__(self, left, op, right):
        raise NotImplementedError()


class Eq_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_eq(self)

    def __str__(self):
        return "EQ_NODE: {} {} {}".format(self.left, self.op, self.right)


class Arith_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_arith(self)

    def __str__(self):
        return "ARITH_NODE: {} {} {}".format(self.left, self.op, self.right)


class Logic_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_logic(self)

    def __str__(self):
        return "LOGIC_NODE: {} {} {}".format(self.left, self.op, self.right)


class Relop_Bin_Node(Bin_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_relop(self)

    def __str__(self):
        return "RELOP_NODE: {} {} {}".format(self.left, self.op, self.right)


class Unary_Node(AST_Node):
    def __init__(self, op, right):
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_unary(self)

    def __str__(self):
        return "UNARY_NODE: {} {}".format(self.op, self.right)


class Bracket_Node(AST_Node):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "BRACKET_NODE: {}".format(self.expr)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_bracket(self)


class ID_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "{}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_id(self)


class Bool_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "BOOL_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_bool(self)


class String_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "STR_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_string(self)


class Num_Node(AST_Node):
    def __init__(self, node_val):
        self.val = node_val

    def __str__(self):
        return "NUM_NODE: {}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_num(self)
