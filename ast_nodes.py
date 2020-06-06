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

    def pprint_nodes(self):
        for stmnt in self.stmnts:
            print(stmnt)


class Bin_Node(AST_Node):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_binary(self)

    def __str__(self):
        return "BIN_NODE: {} {} {}".format(self.left, self.op, self.right)


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


class Bracket_Node(AST_Node):
    def __init__(self, expr):
        self.exrp = expr

    def __str__(self):
        return "{} {}".format(self.expr)

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
        return "{}".format(self.val)

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
        return "{}".format(self.val)

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
        return "{}".format(self.val)

    def accept(self, visitor):
        """
        Keyword Arguments:
        visitor -- The visitor instance used to evaluate the node.
        """
        return visitor.visit_num(self)
